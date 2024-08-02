import graphics as gr
import globals
import equations
import multiprocessing
import functools
import time


def is_greater_than_multi(arr: list, equation: list):
    out = []
    for i in arr:
        out.append(equations.is_greater_than(i[0], i[1], equation))
    return out


def draw_equation_from_matrix(x: int, screenheight: int, matrix: list):
    out = []
    for y in range(screenheight):
        if matrix[x][y] != matrix[x + 1][y] or matrix[x][y] != matrix[x][y + 1] or matrix[x][y] != matrix[x + 1][y + 1]:
            out.append((x, y))
    return out


def main():
    equation = equations.strToEquation(input("Type equation here: "))
    start = time.time()

    globals.window = gr.GraphWin()

    screenDimensions = globals.window.master.winfo_screenwidth(), globals.window.master.winfo_screenheight()
    globals.window.close()
    globals.window = gr.GraphWin("Calculator", screenDimensions[0], screenDimensions[1], autoflush=False)
    globals.window.master.attributes('-fullscreen', True)

    globals.window.update()
    pool = multiprocessing.Pool()

    initTime = time.time()

    greaterThanTable = pool.map(functools.partial(is_greater_than_multi, equation=equation), [[(x-screenDimensions[0]/2, y-screenDimensions[1]/2) for y in range(screenDimensions[1]+1)] for x in range(screenDimensions[0]+1)])

    createTime = time.time()

    for x in range(screenDimensions[0]):
        # globals.window.update()
        for y in range(screenDimensions[1]):
            if greaterThanTable[x][y] != greaterThanTable[x+1][y] or greaterThanTable[x][y] != greaterThanTable[x][y+1] or greaterThanTable[x][y] != greaterThanTable[x+1][y+1]:
                globals.window.plot(x, -y + screenDimensions[1]-1)

    globals.window.update()
    print(time.time() - start, createTime - start, initTime - start)

    globals.window.getMouse()


if __name__ == '__main__':
    main()
