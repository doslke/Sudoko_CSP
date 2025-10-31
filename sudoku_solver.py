import math
import time

from docutils.nodes import section


class SudokuSolver:
    def __init__(self, grid,gui=None):
        self.grid = [row[:] for row in grid]
        self.size = 9
        self.domains={}
        self.gui = gui

    def runs(self):
        self.init_domains()
        self.ac3()
        self.solver(0,0)

    def init_domains(self):
        for i in range(0,9):
            for j in range(0,9):
                self.domains[(i,j)] = self.initial_constraint_propagation(i,j)
                if len(self.domains[(i,j)])==0:
                    raise ValueError(f"Inconsistent puzzle: no possible value at ({i},{j})")

    def initial_constraint_propagation(self,i,j):
        if self.grid[i][j]!=0:
            domain=[self.grid[i][j]]
            return domain
        current_domain=[1,2,3,4,5,6,7,8,9]
        for k in range(0,9):
            if self.grid[i][k]!=0:
                if self.grid[i][k] in current_domain:
                    current_domain.remove(self.grid[i][k])
        for k in range(0,9):
            if self.grid[k][j]!=0:
                if self.grid[k][j] in current_domain:
                    current_domain.remove(self.grid[k][j])
        sections=self.section_divide(i,j)
        for x,y in sections:
            if self.grid[x][y]!=0:
                if self.grid[x][y] in current_domain:
                    current_domain.remove(self.grid[x][y])
        return current_domain

    def section_divide(self,i,j):
        section_index=[]
        section_i=math.ceil((i+1)/3)
        section_j=math.ceil((j+1)/3)
        start_i=(section_i-1)*3
        start_j=(section_j-1)*3
        for k in range(0,3):
            for l in range(0,3):
                if (start_i+k)==i and (start_j+l)==j:
                    continue
                section_index.append((start_i+k,start_j+l))
        return section_index

    def forward_check(self,i,j,val):
        affected_index=[]
        for k in range(0,9):
            if k==j:
                continue
            if val in self.domains[(i,k)]:
                self.domains[(i,k)].remove(val)
                affected_index.append((i,k))
        for k in range(0,9):
            if k==i:
                continue
            if val in self.domains[(k,j)]:
                self.domains[(k,j)].remove(val)
                affected_index.append((k,j))
        for x,y in self.section_divide(i,j):
            if x==i and y==j:
                continue
            if val in self.domains[(x,y)]:
                self.domains[(x,y)].remove(val)
                affected_index.append((x,y))
        return affected_index


    def select_unassigned_variable(self):
        mrv_pos = None
        mrv_size = 10
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    domain_size = len(self.domains[(i, j)])
                    if domain_size < mrv_size:
                        mrv_size = domain_size
                        mrv_pos = (i, j)
        return mrv_pos

    def restore_forward_checking(self,affected,val):
        for x,y in affected:
            if val not in self.domains[(x,y)]:
                self.domains[(x,y)].append(val)

    def order_domain_values(self, x, y):
        value_constraints = []
        for val in self.domains[(x, y)]:
            # 统计如果选 val，会减少多少其他格子的可能性
            count = 0
            for k in range(9):
                if val in self.domains[(x, k)]:
                    count += 1
                if val in self.domains[(k, y)]:
                    count += 1
            for a, b in self.section_divide(x, y):
                if val in self.domains[(a, b)]:
                    count += 1
            value_constraints.append((val, count))
        value_constraints.sort(key=lambda t: t[1])
        return [val for val, _ in value_constraints]

    def get_neighbors(self, i, j):
        neighbors = set()
        for k in range(9):
            if k != j:
                neighbors.add((i, k))
            if k != i:
                neighbors.add((k, j))
        for x, y in self.section_divide(i, j):
            neighbors.add((x, y))
        return neighbors

    def revise(self, xi, xj):
        revised = False
        for val in self.domains[xi][:]:
            if all(val == other for other in self.domains[xj]):
                self.domains[xi].remove(val)
                revised = True
        return revised

    def ac3(self):
        queue = [(xi, xj) for xi in self.domains for xj in self.get_neighbors(*xi)]
        while queue:
            xi, xj = queue.pop(0)
            if self.revise(xi, xj):
                if not self.domains[xi]:
                    return False
                for xk in self.get_neighbors(*xi):
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def solver(self, i, j):
        pos = self.select_unassigned_variable()
        if not pos:
            if self.gui:
                self.gui.update_grid(self.grid)
            return True
        x, y = pos
        for val in self.order_domain_values(x, y):
            self.grid[x][y] = val
            if self.gui:
                self.gui.update_grid(self.grid)
                time.sleep(0.05)
            affected=self.forward_check(x, y, val)
            conflict = any(len(self.domains[pos]) == 0 for pos in affected)
            if not conflict and self.solver(x, y):
                return True
            self.grid[x][y] = 0
            if self.gui:
                self.gui.update_grid(self.grid)
                time.sleep(0.05)
            self.restore_forward_checking(affected,val)
        isSolved=False
        if not isSolved:
            raise Exception(f"THIS IS AN NON-SOLUTION PUZZLE")
        return False