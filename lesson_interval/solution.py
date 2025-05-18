
def build(l:list[int]):
    return [(l[i],l[i+1]) for i in range(0,len(l),2)]
def clip(intervals,bounds):
    clipped=[]
    start_bound,end_bound=bounds
    for s,e in intervals:
        start_clipped=max(s, start_bound)
        end_clipped=min(e,end_bound)
        if start_clipped < end_clipped:
            clipped.append((start_clipped,end_clipped))
    return clipped
def merge(intervals):
    if not intervals:
        return []
    intervals.sort()
    merged=[intervals[0]]
    for c in intervals[1:]:
        last=merged[-1]
        if c[0]<=last[1]:
            merged[-1]=(last[0], max(last[1], c[1]))
        else:
            merged.append(c)
    return merged
def appearance(intervals):
    lesson=tuple(intervals['lesson'])
    pupil_intervals=clip(build(intervals['pupil']),lesson)
    tutor_intervals=clip(build(intervals['tutor']),lesson)

    overlaps=[]
    for p_start,p_end in pupil_intervals:
        for t_start,t_end in tutor_intervals:
            start=max(p_start,t_start)
            end=min(p_end, t_end)
            if start<end:
                overlaps.append((start,end))
    merged=merge(overlaps)
    return sum(end-start for stat,end in merged)
tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

