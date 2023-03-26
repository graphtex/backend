from PIL import Image
import math

UNDIRECTED_BL_TR = 38
UNDIRECTED_BR_TL = 39
DIRECTED_BL_TR = 40
DIRECTED_TR_BL = 41
DIRECTED_BR_TL = 42
DIRECTED_TL_BR = 43

labels = [36., 36., 36., 10., 22., 32., 40., 41., 41., 40.]
boxes = [[427.7503, 427.4237, 477.5254, 477.2537],
         [474.6896, 202.2463, 524.4647, 252.0763],
         [380.3975, 654.5850, 430.1725, 704.4150],
         [441.3253, 441.0137, 463.9503, 463.6637],
         [488.2646, 215.8363, 510.8896, 238.4863],
         [393.9725, 668.1750, 416.5975, 690.8250],
         [457.7220, 251.5509, 494.4930, 427.9492],
         [410.3691, 476.7283, 447.5537, 655.1104],
         [457.7220, 251.5509, 494.4930, 427.9492],
         [410.3691, 476.7283, 447.5537, 655.1104]]
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
    return math.sqrt(p1[0]**2 + p2[0]**2)

def closest_vertex(p, vertex_list):
    closest = min(range(len(vertex_list)), key=lambda i: dist(vertex_list[i], p)) + 1
    return closest


def get_latex(model_output):
    labels = model_output["labels"]
    boxes = model_output["boxes"]
    out_lines = []
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
    return "\n".join(out_lines)


print(get_latex(model_output))
