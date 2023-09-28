from string import digits, ascii_letters, punctuation
import matplotlib.pyplot as plt
import tempfile
import random
from subprocess import run
from json import dumps

printable = digits + ascii_letters + punctuation
RESULT_DIR = './results'
FILE_COUNT = 10
LONG_TEXT_URL = 'https://www.dropbox.com/s/ce83ry9a4d9642z/konstitucija.txt?dl=0'
PAIRS = [
    {'count': 25000, 'length': 10},
    {'count': 25000, 'length': 100},
    {'count': 25000, 'length': 500},
    {'count': 25000, 'length': 1000},
]

HASH_F = [
    {
        'name': 'Rimvydas Civilis',
        'cmd_file': './build/main tf {}',
        'cmd_arg': "./build/main t {}",
        'get_hash_f': lambda x: x.decode('utf-8').split(' ')[4].strip(),
        'get_hash_a': lambda x: x.decode('utf-8').split(' ')[4].strip(),
        'get_time_f': lambda x: float(x.decode('utf-8').split(' ')[2]),
        'get_time_a': lambda x: float(x.decode('utf-8').split(' ')[2]),
        'no_bits': 256,
    }
]

pair_count_sum = sum([pair['count'] for pair in PAIRS])
results = [
    {
        'name': hash_f.get('name', 'Unknown'),
        'not_deterministic_count': 0,
        'size_diff_count': 0,
        'collision_count': 0,
        'hashing_time': [],
        'avg_hex_diff': None,
        'min_hex_diff': None,
        'max_hex_diff': None,
        'avg_bit_diff': None,
        'min_bit_diff': None,
        'max_bit_diff': None,
        'bit_diff_distr': [0] * hash_f.get('no_bits', 256),
        'no_bits': hash_f.get('no_bits', 256),
    } for hash_f in HASH_F
]

def main():
    print('Starting 1st test')
    with tempfile.TemporaryDirectory() as tmpdir:
        print('+ Generating files')
        for i in range(FILE_COUNT):
            with open(tmpdir + f'/1_1_{i}.txt', 'w') as f:
                f.write(random.choice(printable) * 10000)
        for i in range(FILE_COUNT):
            with open(tmpdir + f'/1_2_{i}.txt', 'w') as f:
                f.write(''.join([random.choice(printable) for _ in range(10000)]))
        chars = [random.choice(printable) for _ in range(10000)]
        for i in range(FILE_COUNT):
            with open(tmpdir + f'/1_3_{i}.txt', 'w') as f:
                copy = chars.copy()
                copy[5000] = random.choice(printable)
                f.write(''.join(copy))
        with open(tmpdir + '/1_4_0.txt', 'w') as f:
            pass

        print('+ Running tests')
        for i in range(len(HASH_F)):
            cmd = HASH_F[i]['cmd_file']
            get_hash = HASH_F[i]['get_hash_f']

            for j in range(1, 2):
                for k in range(FILE_COUNT):
                    file_name = tmpdir + f'/1_{j}_{k}.txt'
                    if j == 4 and k != 0: break # There is only one empty file
                    prev_hash = None
                    for _ in range(10):
                        result = run(cmd.format(file_name).split(' '), capture_output=True)
                        hash = get_hash(result.stdout)
                        if prev_hash is not None:
                            if prev_hash != hash:
                                results[i]['not_deterministic_count'] += 1
                            elif len(prev_hash) != len(hash):
                                results[i]['size_diff_count'] += 1
                        prev_hash = hash


    print('Starting 2nd test')
    with tempfile.TemporaryDirectory() as tmpdir:
        print('+ Generating files')
        # Download long text
        run(f'wget -O {tmpdir}/3.txt {LONG_TEXT_URL}'.split(' '), capture_output=True)
        # Splits file into multiple files with line pattern 1,2,4,8...
        with open(tmpdir + '/3.txt', 'r') as f:
            file_content = f.readlines()
        files_length = []
        i = 1
        while i < len(file_content):
            files_length.append(i)
            i *= 2
        files_length.append(len(file_content))
        for i in range(len(files_length)):
            file_length = files_length[i]
            with open(tmpdir + f'/3_{i}.txt', 'w') as f:
                f.writelines(file_content[:file_length])

        print('+ Running tests')
        for i in range(len(HASH_F)):
            cmd = HASH_F[i]['cmd_file']
            get_time = HASH_F[i]['get_time_f']
            for j in range(len(files_length)):
                file_name = tmpdir + f'/3_{j}.txt'
                time_sum = 0
                for _ in range(10):
                    result = run(cmd.format(file_name).split(' '), capture_output=True)
                    time = get_time(result.stdout)
                    time_sum += time
                results[i]['hashing_time'].append({'lines': files_length[j], 'time': time_sum / 5})
    
    graph_time(results)

    print('Starting 3rd test')
    print('+ Running tests')
    for i in range(len(HASH_F)):
        name = HASH_F[i]['name']
        cmd = HASH_F[i]['cmd_arg']
        get_hash = HASH_F[i]['get_hash_a']
        no_bits = HASH_F[i]['no_bits']
        bit_diff_distr = [0] * no_bits
        min_hex_diff = None
        max_hex_diff = None
        avg_hex_diff = 0
        min_bit_diff = None
        max_bit_diff = None
        avg_bit_diff = 0
        for j in range(len(PAIRS)):
            count = PAIRS[j]['count']
            length = PAIRS[j]['length']
            print(f'+++ Running {name} with {length=}')
            for k in range(count):
                if (k+1) % (count//10) == 0:
                    print(f'+++++ {(k+1) * 100 // count}%')
                chars = [random.choice(printable) for _ in range(length)]
                inp_a = ''.join(chars)
                poss_to_change = random.randint(1, length - 1)
                while inp_a[poss_to_change] == chars[poss_to_change]:
                    chars[poss_to_change] = random.choice(printable)
                inp_b = ''.join(chars)
                result_a = run(cmd.format(inp_a).split(' '), capture_output=True)
                result_b = run(cmd.format(inp_b).split(' '), capture_output=True)
                hash_a = get_hash(result_a.stdout)
                hash_b = get_hash(result_b.stdout)
                hex_diff = different_hex(hash_a, hash_b)
                if min_hex_diff is None or hex_diff < min_hex_diff:
                    min_hex_diff = hex_diff
                if max_hex_diff is None or hex_diff > max_hex_diff:
                    max_hex_diff = hex_diff
                avg_hex_diff += hex_diff
                if hash_a == hash_b:
                    results[i]['collision_count'] += 1
                bit_diff = different_bits(hash_a, hash_b, no_bits, bit_diff_distr)
                if min_bit_diff is None or bit_diff < min_bit_diff:
                    min_bit_diff = bit_diff
                if max_bit_diff is None or bit_diff > max_bit_diff:
                    max_bit_diff = bit_diff
                avg_bit_diff += bit_diff
        results[i]['min_hex_diff'] = min_hex_diff
        results[i]['max_hex_diff'] = max_hex_diff
        results[i]['avg_hex_diff'] = avg_hex_diff / pair_count_sum
        results[i]['min_bit_diff'] = min_bit_diff
        results[i]['max_bit_diff'] = max_bit_diff
        results[i]['avg_bit_diff'] = avg_bit_diff / pair_count_sum
        results[i]['bit_diff_distr'] = [x / pair_count_sum for x in bit_diff_distr]

    graph_bit_diff_dist(results)

    with open(f'{RESULT_DIR}/results.json', 'w') as f:
        f.write(dumps(results, indent=2)) # Save results as json

def different_hex(a, b):
    return len([1 for i in range(len(a)) if a[i] != b[i]]) / len(a)

def different_bits(a, b, no_bits, bit_diff_distr):
    a = bin(int(a, 16))[2:]
    a_paddded = '0' * (no_bits - len(a)) + a
    b = bin(int(b, 16))[2:]
    b_paddded = '0' * (no_bits - len(b)) + b
    diff = 0
    for i in range(len(a_paddded)):
        if a_paddded[i] != b_paddded[i]:
            bit_diff_distr[i] += 1
            diff += 1
    return diff / len(a_paddded)

def graph_time(results):
    plt.clf()
    for result in results:
        plt.plot([x['lines'] for x in result['hashing_time']], [x['time'] for x in result['hashing_time']], label=result['name'])
    plt.xlabel('Lines')
    plt.ylabel('Time (ms)')
    plt.legend()
    plt.savefig(f'{RESULT_DIR}/time.png')

def graph_bit_diff_dist(results):
    plt.clf()
    for result in results:
        plt.plot([i for i in range(result['no_bits'])], result['bit_diff_distr'], label=result['name'])
    plt.xlabel('Bit')
    plt.ylabel('Avg. difference percentage')
    plt.yticks([i/10 for i in range(11)])
    plt.legend()
    plt.savefig(f'{RESULT_DIR}/bit_diff_dist.png')

if __name__ == '__main__':
    run(f'mkdir -p {RESULT_DIR}'.split(' '))
    main()
