import collections
import copy
import sys

import decimal

data = collections.OrderedDict()
fo = open('output.txt', 'w')
decision_holder = []
flager = False

def extractVars(network, Y):
    global decision_holder
    variableList = network.keys()
    parentList = []
    # print variableList
    for i in variableList:
        if i not in decision_holder:
            # parentList.append(i)
            #    break
            parentList.append(i)
    # print parentList,'========'
    return parentList


def helper_query(Y, e):
    global decision_holder
    prob = 0.0

    if data[Y]['prob'] != -1:
        if not e[Y]:
            prob = 1.0 - data[Y]['prob']
        if e[Y]:
            prob = data[Y]['prob']
    else:
        ppp = []

        for p in data[Y]['parents']:
            if p in decision_holder:
                if p not in e:
                    return 1.0
            ppp.append(e[p])
        thread = tuple(ppp)

        if not e[Y]:
            prob = 1.0 - data[Y]['condprob'][thread]
        if e[Y]:
            prob = data[Y]['condprob'][thread]

    return prob


def EnumerateAll(variables, e):
    if not variables:
        return 1.0
    Y = variables[0]
    if Y in e:

        val = helper_query(Y, e)
        ret = val * EnumerateAll(variables[1:], e)
    else:
        probs = []
        e2 = copy.deepcopy(e)
        permu = [True, False]
        for y in permu:
            e2[Y] = y
            val = helper_query(Y, e2)
            probs.append(val * EnumerateAll(variables[1:], e2))
        ret = sum(probs)
    # print ret
    return ret


def normalize(dist):
    total = sum(dist)
    return tuple(x / total for x in dist)


def EnumerateAsk(Y, e, network, flag):
    Q = []

    variables = extractVars(network, Y)
    for y in [True, False]:
        e1 = copy.deepcopy(e)
        e1[Y] = y
        Q.append(EnumerateAll(variables, e1))
    return Q


tp = {
    True: '+ ',
    False: '- ',
    (True, True, True): '+ + + ',
    (True, True, False): '+ + - ',
    (True, False, True): '+ - + ',
    (True, False, False): '+ - - ',
    (False, True, True): '- + + ',
    (False, True, False): '- + - ',
    (False, False, True): '- - + ',
    (False, False, False): '- - - ',
    (True, True): '+ + ',
    (True, False): '+ - ',
    (False, True): '- + ',
    (False, False): '- - '

}


def MEU1(inp, extendede, e, data, truth1, MaxEU, flag):
    value = -9999999999
    for truth_value in range(2):
        extendede[inp[0]] = truth1[truth_value]
        MaxEU[getUtilityValue(extendede, e, data, flag)] = truth1[truth_value]
        for i in MaxEU:
            if i > value:
                value = i

    values = MaxEU.keys()
    keys = MaxEU.values()
    maxvalue = -99999
    maxsign = ''

    for i in range(len(MaxEU)):

        if values[i] > maxvalue:
            maxsign = keys[i]
            maxvalue = values[i]

    if 0.5 <= maxvalue < 0.9:
        maxvalue = 1
    if -0.5 <= maxvalue < -0.1:
        maxvalue = -1

    final_ans = decimal.Decimal(str(maxvalue)).quantize(decimal.Decimal())
    if final_ans == -0:
        final_ans = 0

    fo.write(tp[maxsign] + "" + str(final_ans) + '\n')
    # print tp[maxsign], maxvalue


def MEU2(inp, extendede, e, data, truth2, MaxEU, flag):
    value = -999999
    for truth_value in range(4):
        extendede[inp[0]] = truth2[truth_value][0]
        extendede[inp[1]] = truth2[truth_value][1]

        MaxEU[getUtilityValue(extendede, e, data, flag)] = truth2[truth_value]

        for i in MaxEU:
            if i > value:
                value = i

    values = MaxEU.keys()
    keys = MaxEU.values()
    maxvalue = -99999
    maxsign = False

    for i in range(len(MaxEU)):

        if values[i] > maxvalue:
            maxsign = keys[i]
            maxvalue = values[i]
    # print maxsign, maxvalue
    if 0.5 <= maxvalue < 0.9:
        maxvalue = 1
    if -0.5 <= maxvalue < -0.1:
        maxvalue = -1
    final_ans = decimal.Decimal(str(maxvalue)).quantize(decimal.Decimal())
    if final_ans == -0:
        final_ans = 0
    fo.write(tp[maxsign] + "" + str(final_ans) + '\n')


def MEU3(inp, extendede, e, data, truth3, MaxEU, flag):
    value = -999999
    for truth_value in range(8):
        extendede[inp[0]] = truth3[truth_value][0]
        extendede[inp[1]] = truth3[truth_value][1]
        extendede[inp[2]] = truth3[truth_value][2]
        MaxEU[getUtilityValue(extendede, e, data, flag)] = truth3[truth_value]

        for i in MaxEU:
            if i > value:
                value = i

    values = MaxEU.keys()
    keys = MaxEU.values()
    maxvalue = -99999
    maxsign = False

    for i in range(len(MaxEU)):

        if values[i] > maxvalue:
            maxsign = keys[i]
            maxvalue = values[i]
    # print maxsign, maxvalue
    if 0.5 <= maxvalue < 0.9:
        maxvalue = 1
    if -0.5 <= maxvalue < -0.1:
        maxvalue = -1
    final_ans = decimal.Decimal(str(maxvalue)).quantize(decimal.Decimal())
    if final_ans == -0:
        final_ans = 0
    fo.write(tp[maxsign] + "" + str(final_ans) + '\n')


def getUtilityValue(inp, copy_dict_e, data, flag):
    list_value = {'utility': (True,)}
    copy_dict_e1 = copy.deepcopy(copy_dict_e)
    # copy_dict_extendede1 = copy.deepcopy(copy_dict_extendede)

    ans1 = getProbabilityValue(list_value, inp, data, True, {})

    ans2 = getProbabilityValue(copy_dict_e, inp, data, True, {})

    z = copy_dict_e.keys()
    if set(z)<(set(decision_holder)):
        ans2 = 1
    k = ans1/ans2
    return k

def getProbabilityValue(param, copy_dict_e, data, flag, copy_dict_extendede):
    global flager
    result = 1.0
    if flag:
        for i in param:
            copy_dict1 = copy.deepcopy(copy_dict_e)
            if i in copy_dict1:
                copy_dict1.pop(i)

            # print i,'=====1'
            # print copy_dict1,'=========2'
            # print flag,'========3'
            answer = EnumerateAsk(i, copy_dict1, data, flag)

            a = sum(answer) * 100
            if a >= 199:
                if not flager:
                    if param[i]:
                        return normalize(answer)[0]
                    else:
                        return normalize(answer)[1]
                else:
                    return normalize(answer)
            if not flager:
                if param[i]:
                    return answer[0]
                else:
                    return answer[1]
            else:
                return answer

        return result
    else:
        temp1 = 0.0
        temp2 = 0.0
        checker = True
        for value in copy_dict_extendede:
            if checker:

                copy_dict_extendede1 = copy.deepcopy(copy_dict_extendede)
                answer1 = EnumerateAsk(value, copy_dict_extendede1, data, True)
                if not copy_dict_extendede[value]:
                    temp1 = answer1[1]
                if copy_dict_extendede[value]:  # can be copy_dict_extendede1
                    temp1 = answer1[0]
                checker = False
        checker = True
        for value in copy_dict_e:
            if checker:

                copy_dict_e1 = copy.deepcopy(copy_dict_e)
                answer2 = EnumerateAsk(value, copy_dict_e1, data, True)
                z = copy_dict_e.keys()
                if set(z)<set(decision_holder):
                    return temp1
                if not copy_dict_e[value]:
                    temp2 = answer2[1]
                if copy_dict_e[value]:
                    temp2 = answer2[0]
                checker = False

        return temp1 / temp2


def main():
    global data
    global flager
    # content = collections.OrderedDict()
    content = {}
    truth = {
        '+': (True,),
        '-': (False,),
        '+ + +': (True, True, True),
        '+ + -': (True, True, False),
        '+ - +': (True, False, True),
        '+ - -': (True, False, False),
        '- + +': (False, True, True),
        '- + -': (False, True, False),
        '- - +': (False, False, True),
        '- - -': (False, False, False),
        '+ +': (True, True),
        '+ -': (True, False),
        '- +': (False, True),
        '- -': (False, False)

    }
    queries = []
    first_flag = True
    second_flag = False
    third_flag = False
    six_star_flag = True
    # fh = open('input.txt', 'r')
    fh = open(sys.argv[2], 'r')
    single_flag = True
    z = ''
    for line in fh:
        if first_flag:
            if line.startswith("******"):
                # print line
                first_flag = False
                second_flag = True
                continue
            # print 'first part'
            queries.append(line.strip())

        if second_flag:
            if line.startswith("******"):
                # print line
                second_flag = False
                third_flag = True
                content = {}  # not required if utility handled
                continue
            if line.startswith("***"):
                # print line
                content = {}
                # content = collections.OrderedDict()
                counter = 0
                continue

            if line.startswith('decision'):
                data[z]['prob'] = 1
                decision_holder.append(z)
                continue

            if line.find(" | ") < 0 and line[0].isalpha():
                # print line,'==============='
                single_flag = True
                content['parents'] = []
                content['condprob'] = {}
                z = line.strip()
                data[line.strip()] = content

                continue

            elif line.find(" | ") > 0 and line[0].isalpha():
                single_flag = False
                left_side = line.strip().split(" | ")[0]
                right_side = line.strip().split(" | ")[1].split(" ")
                evidence_length = len(right_side)
                content['parents'] = right_side
                content['prob'] = -1
                content['condprob'] = {}
                data[left_side] = content
                z = line.strip()
                continue

            if single_flag:
                content['prob'] = float(line.strip())
            else:
                right_part = line.strip()
                probability = right_part[0:right_part.find(" ")].strip()
                sign = right_part[right_part.find(" "):len(right_part)].strip()
                content['condprob'][truth[sign]] = float(probability)

        if third_flag:
            if line.startswith("utility"):
                left_side = line.strip().split(" | ")[0]
                right_side = line.strip().split(" | ")[1].split(" ")
                content['parents'] = right_side
                content['prob'] = -1
                content['condprob'] = {}
                data[left_side] = content
            else:
                # print line.strip()
                a = line.strip()
                position = a.index(" ")
                value = int(a[0:position])
                sign = a[position + 1:len(line.strip())]
                content['condprob'][truth[sign]] = value
    fh.close()

    # print data
    for query in queries:
        e = collections.OrderedDict()
        extendede = collections.OrderedDict()
        if query[0] == "P":
            flager = True
            if query.find("|") > 0:
                Q = query[2:len(query) - 1]
                left_part = Q.split(" | ")[0]
                right_part = Q.split(" | ")[1]
                main_query = left_part[0:left_part.index(" ")]
                main_query_sign = left_part[-1]
                evidences = right_part.split(", ")

                if "," in left_part:
                    left_variables = left_part.split(", ")
                    for left_var in left_variables:
                        left_query = left_var[0:left_var.index(" ")].strip()
                        left_query_sign = left_var[-1].strip()
                        if main_query_sign == "+":
                            extendede[left_query] = True
                        else:
                            extendede[left_query] = False

                if main_query_sign == "+":
                    extendede[main_query] = True
                else:
                    extendede[main_query] = False

                for evidence in evidences:
                    main_evidence = evidence[0:evidence.index(" ")].strip()
                    main_evidence_sign = evidence[-1].strip()
                    # print 'main evidence sign', main_evidence_sign
                    if main_evidence_sign == "+":
                        e[main_evidence] = True
                        extendede[main_evidence] = True
                    else:
                        e[main_evidence] = False
                        extendede[main_evidence] = False

                copy_dict_e = copy.deepcopy(e)
                copy_dict_extendede = copy.deepcopy(extendede)

                answer = getProbabilityValue(main_query, copy_dict_e, data, False, copy_dict_extendede)
                final_ans = decimal.Decimal(str(answer)).quantize(decimal.Decimal('.01'))
                fo.write(str(final_ans) + '\n')
                flager = False


            else:

                Q = query[2:len(query) - 1]
                evidences = Q.split(", ")
                main_query = evidences[0].strip()[0:evidences[0].index(" ")]
                main_query_sign = evidences[0][-1]
                if main_query_sign == "+":
                    extendede[main_query] = True
                else:
                    extendede[main_query] = False

                for evidence in evidences:

                    main_evidence = evidence[0:evidence.index(" ")].strip()
                    main_evidence_sign = evidence[-1].strip()
                    if main_evidence_sign == "+":
                        e[main_evidence] = True
                        extendede[main_evidence] = True
                    else:
                        e[main_evidence] = False
                        extendede[main_evidence] = False

                # print e
                copy_dict_e = copy.deepcopy(e)
                copy_dict_extendede = copy.deepcopy(extendede)

                answer = getProbabilityValue(main_query, copy_dict_e, data, True, copy_dict_extendede)
                if main_query_sign == "+":
                    final_ans = decimal.Decimal(str(answer[0])).quantize(decimal.Decimal('.01'))
                    fo.write(str(final_ans) + '\n')
                else:

                    final_ans = decimal.Decimal(str(answer[1])).quantize(decimal.Decimal('.01'))
                    fo.write(str(final_ans) + '\n')

                flager = False

        if query[0] == "E":
            Q = query[3:len(query) - 1]
            if query.find("|") > 0:
                left_part = Q.split(" | ")[0]
                right_part = Q.split(" | ")[1]
                main_query = left_part[0:left_part.index(" ")]
                main_query_sign = left_part[-1]
                evidences = right_part.split(", ")
                if "," in left_part:
                    left_variables = left_part.split(", ")
                    for left_var in left_variables:
                        left_query = left_var[0:left_var.index(" ")].strip()
                        left_query_sign = left_var[-1].strip()
                        if main_query_sign == "+":
                            extendede[left_query] = True
                        else:
                            extendede[left_query] = False

                if main_query_sign == "+":
                    extendede[main_query] = True
                else:
                    extendede[main_query] = False

                for evidence in evidences:
                    main_evidence = evidence[0:evidence.index(" ")].strip()
                    main_evidence_sign = evidence[-1].strip()
                    if main_evidence_sign == "+":
                        e[main_evidence] = True
                        extendede[main_evidence] = True
                    else:
                        e[main_evidence] = False
                        extendede[main_evidence] = False

                # print e
                copy_dict_e = copy.deepcopy(e)
                copy_dict_extendede = copy.deepcopy(extendede)
                answer = getUtilityValue(copy_dict_extendede, copy_dict_e, data, False)
                final_ans = decimal.Decimal(str(answer)).quantize(decimal.Decimal())
                fo.write(str(final_ans) + '\n')

            else:
                Q = query[3:len(query) - 1]
                evidences = Q.split(", ")
                main_query = evidences[0].strip()[0:evidences[0].index(" ")]
                main_query_sign = evidences[0][-1]
                # print main_query
                if main_query_sign == "+":
                    extendede[main_query] = True
                else:
                    extendede[main_query] = False

                for evidence in evidences:

                    main_evidence = evidence[0:evidence.index(" ")].strip()
                    main_evidence_sign = evidence[-1].strip()
                    if main_evidence_sign == "+":
                        # e[main_evidence] = True
                        extendede[main_evidence] = True
                    else:
                        # e[main_evidence] = False
                        extendede[main_evidence] = False

                copy_dict_e = copy.deepcopy(e)
                copy_dict_extendede = copy.deepcopy(extendede)

                answer = getUtilityValue(copy_dict_extendede, copy_dict_e, data, False)
                final_ans = decimal.Decimal(str(answer)).quantize(decimal.Decimal())
                fo.write(str(final_ans) + '\n')

        if query[0] == "M":
            Q = query[4:len(query) - 1]

            if query.find(" | ") > 0:
                flag = False
                left_part = Q.split(" | ")[0]
                right_part = Q.split(" | ")[1]

                inp = left_part.split(", ")
                # print inp,' with pipe'

                evidences = right_part.split(", ")

                for evidence in evidences:
                    main_evidence = evidence[0:evidence.index(" ")].strip()
                    main_evidence_sign = evidence[-1].strip()
                    if main_evidence_sign == "+":
                        e[main_evidence] = True
                        extendede[main_evidence] = True
                    else:
                        e[main_evidence] = False
                        extendede[main_evidence] = False
            else:
                e = {}
                flag = True
                inp = Q.split(", ")
                # print inp,'without pipe'
            truth3 = [(True, True, True), (True, True, False),
                      (True, False, True), (True, False, False),
                      (False, True, True), (False, True, False),
                      (False, False, True), (False, False, False)]
            truth1 = (True, False)
            truth2 = [(True, True), (True, False), (False, True), (False, False)]
            MaxEU = {}

            copy_dict = copy.deepcopy(e)

            if len(inp) == 1:
                MEU1(inp, extendede, copy_dict, data, truth1, MaxEU, flag)
            if len(inp) == 2:
                MEU2(inp, extendede, copy_dict, data, truth2, MaxEU, flag)
            if len(inp) == 3:
                MEU3(inp, extendede, copy_dict, data, truth3, MaxEU, flag)


if __name__ == "__main__":
    main()
