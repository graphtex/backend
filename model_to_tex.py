from PIL import Image
import math

UNDIRECTED_BL_TR = 38
UNDIRECTED_BR_TL = 39
DIRECTED_BL_TR = 40
DIRECTED_TR_BL = 41
DIRECTED_BR_TL = 42
DIRECTED_TL_BR = 43

labels = [36., 36., 36., 36., 35.,  5., 21., 17., 39., 39., 38., 38., 39.]
boxes = [[532.8818, 461.5436, 582.6569, 511.3736],
         [322.3549, 394.5907, 372.1299, 444.4207],
         [499.4940, 201.6207, 549.2690, 251.4507],
         [355.7192, 654.5850, 405.4942, 704.4150],
         [546.4568, 475.1336, 569.0818, 497.7836],
         [335.9299, 408.1807, 358.5549, 430.8307],
         [513.0690, 215.2107, 535.6940, 237.8607],
         [369.2942, 668.1750, 391.9192, 690.8250],
         [370.9619, 427.0491, 534.0499, 478.9152],
         [527.5558, 251.2472, 554.5951, 461.7471],
         [364.0825, 244.8808, 507.5414, 401.1606],
         [397.4446, 504.8057, 540.9314, 661.1530],
         [350.4136, 444.2177, 377.4355, 654.7881]]
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
