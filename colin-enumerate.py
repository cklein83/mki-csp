# @title
def enumerate_solutions(week_name, programs, k=3, time_limit=10.0):
    found = []
    for i in range(k):
        # jede bereits gefundene Lösung ausschließen
        def blocking(model, y, count, programs_, found_=found):
            for prev in found_:
                # prev ist ein dict {(d,t,r): s}
                # -> wir bauen die zugehörigen y-Variablen (s,d,t,r)
                vars_prev = []
                for (d, t, r), s in prev.items():
                    if (s, d, t, r) in y:
                        vars_prev.append(y[(s, d, t, r)])
                if vars_prev:
                    # mindestens eine dieser Variablen darf nicht 1 sein
                    model.Add(sum(vars_prev) <= len(vars_prev) - 1)
        sched, solver, status = solve_week(week_name, programs, time_limit=time_limit,
                                           extra_constraints=blocking)
        if sched is None:
            break
        found.append(sched)
    return found

wname = list(weeks.keys())[0]  # Woche 1 als Beispiel
programs = weeks[wname]
sols = enumerate_solutions(wname, programs, k=3)
print(f'{len(sols)} unterschiedliche Lösungen für {wname}\n')
for i, s in enumerate(sols):
    print(f'--- Lösung {i+1} ---')
    print_schedule(s, programs)
    validate(s, programs, verbose=True)
    print()