from PIL import Image
import math

UNDIRECTED_BL_TR = 38
UNDIRECTED_BR_TL = 39
DIRECTED_BL_TR = 40
DIRECTED_TR_BL = 41
DIRECTED_BR_TL = 42
DIRECTED_TL_BR = 43

labels = [36., 36., 36.,  4., 33., 12., 39., 39., 38.]
boxes = [[239.4992, 301.2668, 289.2742, 351.0968],
         [631.3757, 328.4032, 681.1507, 378.2332],
         [411.9626, 654.5850, 461.7376, 704.4150],
         [253.0742, 314.8568, 275.6992, 337.5068],
         [644.9507, 341.9932, 667.5757, 364.6432],
         [425.5376, 668.1750, 448.1626, 690.8250],
         [289.2149, 327.9011, 631.4351, 351.5989],
         [275.3135, 348.5670, 425.9233, 657.1147],
         [450.7515, 373.9841, 642.3618, 658.8340]]
model_output = {'labels': labels, 'boxes': boxes}

node_line = "\\node[main] (%i) at (%f,%f) {$%s$};"
UNDIRECTED_LINE = "\draw (%i) -- (%i);"
DIRECTED_LINE = "\draw[->] (%i) -- (%i);"

X_RANGE = 4
Y_RANGE = 4

code_to_letter = {}
for i in range(48, 58):
    code_to_letter[i - 48] = chr(i)
for i in range(97, 123):
    code_to_letter[i - 87] = chr(i)

def dist(p1, p2):
    return math.sqrt(float(p1[0] - p2[0])**2 + float(p2[1] - p2[0])**2)

def closest_vertex(p, vertex_list):
    closest = min(range(len(vertex_list)), key=lambda i: dist(vertex_list[i], p)) + 1
    return closest


def get_latex(model_output):
    labels = model_output["labels"]
    boxes = model_output["boxes"]
    out_lines = [r'\begin{tikzpicture}[thick,main/.style = {draw, circle}]']
    max_x = max([boxes[i][2] if int(labels[i]) == 36 else 0 for i in range(len(boxes))])
    max_y = max([boxes[i][3] if int(labels[i]) == 36 else 0 for i in range(len(boxes))])
    for i in range(len(boxes)):
        boxes[i][1] = max_y - boxes[i][1]
        boxes[i][3] = max_y - boxes[i][3]

    # First draw nodes
    num_node = 1
    vertex_list = []
    for i in range(len(labels)):
        if labels[i] <= 35:
            out_lines.append(node_line % (num_node, boxes[i][0] / float(max_x) * X_RANGE, boxes[i][1] / float(max_y) * Y_RANGE, code_to_letter[labels[i]]))
            vertex_list.append([boxes[i][0], boxes[i][1]])
            num_node += 1

    # Draw edges
    for i in range(len(labels)):
        BL = (boxes[i][0], boxes[i][3])
        BR = (boxes[i][2], boxes[i][3])
        TL = (boxes[i][0], boxes[i][1])
        TR = (boxes[i][2], boxes[i][1])
        if labels[i] == UNDIRECTED_BL_TR:
            out_lines.append(UNDIRECTED_LINE % (closest_vertex(BL, vertex_list), closest_vertex(TR, vertex_list)))
        elif labels[i] == UNDIRECTED_BR_TL:
            out_lines.append(UNDIRECTED_LINE % (closest_vertex(TL, vertex_list), closest_vertex(BR, vertex_list)))
        elif labels[i] == DIRECTED_BL_TR:
            out_lines.append(DIRECTED_LINE % (closest_vertex(BL, vertex_list), closest_vertex(TR, vertex_list)))
        elif labels[i] == DIRECTED_TR_BL:
            out_lines.append(DIRECTED_LINE % (closest_vertex(TR, vertex_list), closest_vertex(BL, vertex_list)))
        elif labels[i] == DIRECTED_BR_TL:
            out_lines.append(DIRECTED_LINE % (closest_vertex(BR, vertex_list), closest_vertex(TL, vertex_list)))
        elif labels[i] == DIRECTED_TL_BR:
            out_lines.append(DIRECTED_LINE % (closest_vertex(TL, vertex_list), closest_vertex(BR, vertex_list)))
    out_lines.append(r'\end{tikzpicture}')
    return "\n".join(out_lines)


print(get_latex(model_output))
