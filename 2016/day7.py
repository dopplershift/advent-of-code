def parse_ip(ip):
    blocks = []
    hypernets = []
    while ip:
        hyper_start = ip.find('[')
        if hyper_start == -1:
            blocks.append(ip)
            break
        else:
            blocks.append(ip[:hyper_start])
        hyper_end = ip.find(']', hyper_start + 1)
        hypernets.append(ip[hyper_start + 1:hyper_end])
        ip = ip[hyper_end + 1:]
    return blocks, hypernets


def has_abba(s):
    for ind in range(len(s) - 3):
        if (s[ind] != s[ind + 1] and
            s[ind] == s[ind + 3] and
            s[ind + 1] == s[ind + 2]):
            return True
    return False


def supports_tls(ip):
    blocks, hypernets = parse_ip(ip)
    return not any(has_abba(b) for b in hypernets) and any(has_abba(b) for b in blocks)


def find_abas(s):
    for ind in range(len(s) - 2):
        if s[ind] == s[ind + 2] != s[ind + 1]:
            yield s[ind:ind + 3]


def aba_to_bab(s):
    return s[1] + s[:2]


def supports_ssl(ip):
    blocks, hypernets = parse_ip(ip)
    babs = set(bab for b in hypernets for bab in find_abas(b))

    return any(aba_to_bab(aba) in babs
               for b in blocks for aba in find_abas(b))


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert supports_tls('abba[mnop]qrst')
    assert supports_tls('abcd[bdab]xyyx')
    assert not supports_tls('abcd[bddb]xyyx')
    assert not supports_tls('aaaa[qwer]tyui')
    assert supports_tls('ioxxoj[asdfgh]zxcvbn')

    assert supports_ssl('aba[bab]xyz')
    assert not supports_ssl('xyx[xyx]xyx')
    assert supports_ssl('aaa[kek]eke')
    assert supports_ssl('zazbz[bzb]cdb')

    puz = Puzzle(2016, 7)

    puz.answer_a = sum(supports_tls(ip) for ip in puz.input_data.split('\n'))
    print('Part 1:', puz.answer_a)

    puz.answer_b = sum(supports_ssl(ip) for ip in puz.input_data.split('\n'))
    print('Part 2:', puz.answer_b)
