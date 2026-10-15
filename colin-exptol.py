wname = list(weeks.keys())[0]
programs = weeks[wname]

for tol in [2.0, 1.0, 0.5, 0.3]:
    sched, solver, status = solve_week(wname, programs, pop_tol=tol, time_limit=10.0)
    status_str = {cp_model.OPTIMAL: 'OPTIMAL',
                  cp_model.FEASIBLE: 'FEASIBLE',
                  cp_model.INFEASIBLE: 'INFEASIBLE',
                  cp_model.UNKNOWN: 'UNKNOWN'}.get(status, str(status))
    print(f'Popularitäts-Toleranz {tol}: Status = {status_str}')