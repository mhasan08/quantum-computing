import cmath
import math
import random

import matplotlib.pyplot as plt


def number_of_qubits(n):
    qubits = 2 * math.ceil(math.log(n, 2))
    return qubits


def gcd(a, b):
    return math.gcd(a, b)


def choose_residue(n_qubits, x, n):
    list_residue_all = []
    list_residue_dist = []
    span = 2 ** n_qubits
    count = 0
    for r in range(0, span):
        residue = (x ** r) % n
        list_residue_all.append(residue)
        if residue == 1 and count == 0:
            list_residue_dist.append(residue)
            count = count +1
        elif residue == 1 and count == 1:
            count = count + 1
        elif count == 1:
            list_residue_dist.append(residue)
    print(list_residue_dist)
    size = len(list_residue_dist)
    random_index = random.randint(1, size - 1)
    return list_residue_dist[random_index], int(span / size)


def get_probability_index_list(list_probability):
    sentinel = -1.0000
    index = 0
    list_index = []
    for p_index in range(2, len(list_probability)):
        if list_probability[p_index] > sentinel:
            sentinel = list_probability[p_index]
            index = p_index
    list_index.append(index)
    print(list_index)
    for p_index in range(index + 1, len(list_probability)):
        if list_probability[p_index] == list_probability[index]:
            list_index.append(p_index)

    # can take some lower probabilities as well
    # omitted here

    return list_index


def continued_fraction(a, b, list_c_f):
    if a == 1 or a == 0:
        return
    gcd = math.gcd(a, b)
    if gcd != 1:
        a = int(a / gcd)
        b = int(b / gcd)
    quo = int(b / a)
    res = b % a
    list_c_f.append(quo)
    if res == 1:
        list_c_f.append(a)
    else:
        continued_fraction(res, a, list_c_f)


factor_found = False


def check_factor(x, r, n):
    #print("#######")
    #print("x = %d; r = %d" % (x, r))
    fp = (x ** (r/2) + 1) % n
    if fp == 0:
        print("false positive")
        return
    x_1 = ((x ** (r / 2)) % n) - 1
    x_2 = ((x ** (r / 2)) % n) + 1
    f1 = gcd(int(x_1), n)
    f2 = gcd(int(x_2), n)

    #print("f1 = %d; f2 = %d" %(f1, f2))

    if f1 == 1 and f2 == 1:
        return

    global factor_found

    if n % f1 == 0 and f1 != 1 and f1 != n:
        print("p = %d" % f1)
        print("q = %d" % (n / f1))
        factor_found = True
    elif f2 != 1 and f2 != n:
        print("p = %d" % f2)
        print("q = %d" % (n / f2))
        factor_found = True


def factorize(x, n, list_fraction):
    print(list_fraction)
    cf_len = len(list_fraction)
    list_s = []
    list_r = []
    list_s.append(list_fraction[0])
    list_s.append(1 + list_fraction[0]*list_fraction[1])

    list_r.append(1)
    list_r.append(list_fraction[1])

    if list_r[1] % 2 == 0 and gcd(list_s[1], list_r[1]) == 1:
        check_factor(x, list_r[1], n)
    else:
        for i in range(2, len(list_r) - 1):
            if factor_found:
                break
            if list_r[i] % 2 == 0 and gcd(list_s[i], list_r[i]) == 1:
                check_factor(x, list_r[i], n)


def find_factors(n):
    qubits = number_of_qubits(n)
    x = random.randint(2, n - 1)

    if gcd(x, n) != 1:
        p = gcd(x, n)
        q = n / p
        print("p = %d" % p)
        print("q = %d" % q)
    else:
        print("finding random residue ....")
        c_residue, size = choose_residue(qubits, x, n)
        print("residue => %d; size = %d" % (c_residue, size))

        list_mod = []
        list_mod_index = []
        ft_span = 2 ** qubits
        for r in range(0, ft_span):
            residue = (x ** r) % n
            if residue == c_residue:
                list_mod.append(residue)
                list_mod_index.append(r)
        print(list_mod_index)
        print(list_mod)

        list_fft_exp = []
        list_probability = []

        for ft in range(0, int(ft_span)):
            exp = 0
            for mod_index in range(0, size):
                exp = exp + cmath.exp(-2 * cmath.pi * 1j * ft * list_mod_index[mod_index] / ft_span)
            if round(exp.real, 8) != 0:
                #print("ft => %d; real => %f; img => %f" % (ft, exp.real, exp.imag))
                #print("ft => %d; abs => %d" % (ft, abs(exp)))

                list_fft_exp.append(abs(exp))
                list_probability.append(abs(exp) / ft_span)

            else:
                list_fft_exp.append(0)
                list_probability.append(0)

        f = plt.figure(1)
        plt.plot(list_fft_exp, linestyle='-', marker='+', color='r')
        f.show()

        g = plt.figure(2)
        plt.plot(list_probability, linestyle='-', marker='+', color='r')
        g.show()

        list_probability_index = get_probability_index_list(list_probability)
        print(list_probability_index)

        global factor_found

        for i in range(0, len(list_probability_index)):
            if factor_found:
                break
            list_continued_fraction = []
            list_continued_fraction.append(0)
            continued_fraction(list_probability_index[i], ft_span, list_continued_fraction)
            factorize(x, n, list_continued_fraction)

        if not factor_found:
            print("uhh, all probable probabilities exhausted !!")


if __name__ == "__main__":
    n = 91
    if n % 2 != 0:
        find_factors(n)
    else:
        print("n is even ...")