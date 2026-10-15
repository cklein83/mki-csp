# Begründung der Modellierung: Slot als Variable, Studiengang als Wert

## Gewählte Modellierung

Für jede Prüfungswoche *w* wird ein eigenes CSP (X, Dom_w, C) aufgestellt:

- **X** = { x_{d,t,r} | d ∈ {Mo, …, Fr}, t ∈ {A, B, C, D}, r ∈ {R1, R2} }, also 40 Variablen (im Code `"Mo_A_R1"` … `"Fr_D_R2"`)
- **Dom_w** = Studiengänge, die in Woche *w* beteiligt sind (z. B. Dom_W2 = {ET, MB, MT, DS})
- **C** = Bedarf, faire Verteilung attraktiver Termine, parallele bzw. aufeinanderfolgende Termine

Die Woche ist kein Teil der Variablen. Die Wochen sind voneinander unabhängig und werden deshalb als getrennte CSPs gelöst.

## Verworfene Alternative: Studiengang als Variable, Slot als Wert

Denkbar wäre die umgekehrte Zuordnung: Jeder Studiengang ist eine Variable, und seine Domäne besteht aus den Tupeln (Woche, Tag, Slot, Raum).

```python
domain = [(week, day, slot, room) for week in weeks for day in weekdays
          for slot in slots for room in rooms]
for program in study_programs:
    csp.addVariable(program, domain)
```

Diese Modellierung ist aus folgenden Gründen ungeeignet:

1. **Ein Studiengang bekäme genau einen Slot.** Eine CSP-Variable nimmt genau einen Wert an. Laut Bedarfsberechnung braucht ein Studiengang aber $n_s$ Slots, z. B. MB in Woche 1 16 von 40.

2. **Mengenwertige Domänen wären nötig.** Um mehrere Slots abzubilden, müsste die Domäne aus Teilmengen der 40 Slots bestehen. Allein für MB mit 16 Slots gibt es $\binom{40}{16} \approx 6{,}3 \cdot 10^{10}$ mögliche Werte, für einen Studiengang mit 8 Slots immer noch $\binom{40}{8} \approx 7{,}7 \cdot 10^{7}$.

3. **Zusätzliche Constraints gegen Doppelbelegung.** Dass ein Raum zu einem Zeitpunkt nur einem Studiengang gehört, müsste über paarweise Disjunktheit der Slot-Mengen aller Studiengänge erzwungen werden.

4. **Unabhängige Wochen werden vermischt.** Mit der Woche im Tupel enthält ein einziges CSP alle drei Wochen. Der Suchraum wird größer, obwohl die Wochen nichts miteinander zu tun haben.

## Vorteile der gewählten Modellierung

- **„Ein Raum ist zu einem Zeitpunkt nur einem Studiengang zugeordnet“** gilt implizit: Jede Variable x_{d,t,r} hat genau einen Wert. Dafür ist kein eigener Constraint nötig.
- **„Nur beteiligte Studiengänge erhalten Slots“** ist über die wochenspezifische Domäne Dom_w erfüllt.
- **Der Bedarf** lässt sich als Zähl-Constraint über alle 40 Variablen formulieren: $\lfloor 40\,q_s \rfloor \le |\{x \in X : x = s\}| \le \lceil 40\,q_s \rceil$ mit $q_s = g_s / \sum_{j \in W} g_j$. Dieselbe Regel gilt für die 8 Slots jedes Tages. In CP-SAT ist das jeweils eine lineare Summe über Boolesche Variablen $x_{v,s}$.
- **Präferenzen und Terminstruktur** lassen sich direkt formulieren, weil Tag, Slot und Raum im Variablennamen stehen:
  - Attraktivität: Zähl-Constraint nur über die Variablen der attraktiven Termine
  - Parallel: x_{d,t,R1} = x_{d,t,R2}
  - Aufeinanderfolgend: x_{d,t,r} = x_{d,t+1,r}
- **Die Modellierung entspricht dem Vorschlag der Aufgabenstellung:** „jeder Kombination aus Wochentag, Zeitslot und Raum eine Variable zuzuordnen, deren Wert den zugeordneten Studiengang angibt“.
