import os
import re
import sys
import graphviz

# function to create control flow graph and save as pdf
def create_control_flow_graph(file_path):
    # read the file
    with open(file_path, "r") as file:
        code = file.read()

    # create a graph
    graph = graphviz.Digraph(comment="Control Flow Graph")
    
    # add nodes
    lines = code.split("\n")
    for i, line in enumerate(lines):
        node_label = f"{i+1}. {line}"
        graph.node(str(i), label=node_label)

    # add edges
    for i, line in enumerate(lines):
        if "if" in line:
            # find the line number of the next else or end-if statement
            j = i + 1
            while j < len(lines):
                if "else" in lines[j] or "end-if" in lines[j]:
                    break
                j += 1
            # add edges
            graph.edge(str(i), str(j))
            graph.edge(str(i), str(i+1))
            graph.edge(str(j), str(i+1))
        elif "for" in line or "while" in line:
            # find the line number of the next end-for or end-while statement
            j = i + 1
            while j < len(lines):
                if "end-for" in lines[j] or "end-while" in lines[j] or "break" in lines[j]:
                    break
                j += 1
            # add edges
            graph.edge(str(i), str(j))
            graph.edge(str(i), str(i+1))
            graph.edge(str(j), str(i))
        elif "break" in line:
            # find the line number of the next statement
            j = i + 1
            while j < len(lines):
                if "end-for" not in lines[j] and "end-while" not in lines[j] and "break" not in lines[j]:
                    break
                j += 1
            # add edges
            graph.edge(str(i), str(j))
        else:
            # add a simple edge
            graph.edge(str(i), str(i+1))

    # render and save the graph as pdf
    graph.format = "pdf"
    graph.render(filename="Result\\Control_Flow_Graph")
    

"""
def main():
    # Create control flow graph and save as pdf
    create_control_flow_graph(file_path)
    print("Control Flow Graph saved as Control_Flow_Graph.pdf")
    
if __name__ == '__main__':
    main()"""