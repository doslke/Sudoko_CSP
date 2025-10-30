import math

from docutils.nodes import section


class SudokuSolver:
    def __init__(self, grid):
        self.grid = [row[:] for row in grid]
        self.size = 9
        self.domains={}

    def display(self):
        self.init_domains()
        for i in range(0,9):
            for j in range(0,9):
                print(self.domains[(i,j)])
            print("\n")

    def init_domains(self):
        for i in range(0,9):
            for j in range(0,9):
                self.domains[(i,j)] = self.initial_constraint_propagation(i,j)

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
            if val in self.domains[(i,k)]:
                self.domains[(i,k)].remove(val)
                affected_index.append((i,k))
        for k in range(0,9):
            if val in self.domains[(k,j)]:
                self.domains[(k,j)].remove(val)
                affected_index.append((k,j))
        for x,y in self.section_divide(i,j):
            if val in self.domains[(x,y)]:
                self.domains[(x,y)].remove(val)
                affected_index.append((x,y))
        return affected_index

    def find_empty(self,i,j):
        x=i
        y=j
        while x<9:
            if y>8:
                y=0
                x+=1
            if self.grid[x][y]==0:
                return x,y
            y+=1
        return None

    def solver(self,i,j):
        if i>=9:
            return True
        if self.grid



