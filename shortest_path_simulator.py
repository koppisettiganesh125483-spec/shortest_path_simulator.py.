import tkinter as tk
from tkinter import ttk, messagebox
import heapq


class ShortestPathSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Shortest Path Simulator")
        self.root.geometry("850x650")
        self.root.configure(bg="#f0f4f8")

        self.graph = {}

        title = tk.Label(
            root,
            text="SHORTEST PATH SIMULATOR",
            font=("Arial", 22, "bold"),
            bg="#17365D",
            fg="white",
            pady=15
        )
        title.pack(fill="x")

        main_frame = tk.Frame(root, bg="#f0f4f8")
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Edge input section
        edge_frame = tk.LabelFrame(
            main_frame,
            text="Add Nodes and Edges",
            font=("Arial", 12, "bold"),
            bg="#f0f4f8",
            padx=10,
            pady=10
        )
        edge_frame.pack(fill="x", pady=5)

        tk.Label(edge_frame, text="Source:", bg="#f0f4f8").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.source_entry = tk.Entry(edge_frame, width=12)
        self.source_entry.grid(row=0, column=1, padx=5)

        tk.Label(edge_frame, text="Destination:", bg="#f0f4f8").grid(
            row=0, column=2, padx=5
        )
        self.destination_entry = tk.Entry(edge_frame, width=12)
        self.destination_entry.grid(row=0, column=3, padx=5)

        tk.Label(edge_frame, text="Distance:", bg="#f0f4f8").grid(
            row=0, column=4, padx=5
        )
        self.distance_entry = tk.Entry(edge_frame, width=10)
        self.distance_entry.grid(row=0, column=5, padx=5)

        tk.Button(
            edge_frame,
            text="Add Edge",
            command=self.add_edge,
            bg="#198754",
            fg="white",
            width=12
        ).grid(row=0, column=6, padx=5)

        # Example graph button
        tk.Button(
            edge_frame,
            text="Load Example",
            command=self.load_example,
            bg="#0d6efd",
            fg="white"
        ).grid(row=1, column=1, pady=10)

        tk.Button(
            edge_frame,
            text="Clear Graph",
            command=self.clear_graph,
            bg="#dc3545",
            fg="white"
        ).grid(row=1, column=3, pady=10)

        # Graph information
        graph_frame = tk.LabelFrame(
            main_frame,
            text="Graph Connections",
            font=("Arial", 12, "bold"),
            bg="#f0f4f8",
            padx=10,
            pady=10
        )
        graph_frame.pack(fill="both", expand=True, pady=8)

        self.graph_display = tk.Text(
            graph_frame,
            height=7,
            font=("Consolas", 11),
            wrap="word"
        )
        self.graph_display.pack(fill="both", expand=True)

        # Shortest path selection
        path_frame = tk.LabelFrame(
            main_frame,
            text="Find Shortest Path",
            font=("Arial", 12, "bold"),
            bg="#f0f4f8",
            padx=10,
            pady=10
        )
        path_frame.pack(fill="x", pady=5)

        tk.Label(path_frame, text="Start Node:", bg="#f0f4f8").grid(
            row=0, column=0, padx=5, pady=5
        )

        self.start_combo = ttk.Combobox(
            path_frame, width=12, state="readonly"
        )
        self.start_combo.grid(row=0, column=1, padx=5)

        tk.Label(path_frame, text="End Node:", bg="#f0f4f8").grid(
            row=0, column=2, padx=5
        )

        self.end_combo = ttk.Combobox(
            path_frame, width=12, state="readonly"
        )
        self.end_combo.grid(row=0, column=3, padx=5)

        tk.Button(
            path_frame,
            text="Find Shortest Path",
            command=self.find_shortest_path,
            bg="#17365D",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10
        ).grid(row=0, column=4, padx=10)

        # Results
        result_frame = tk.LabelFrame(
            main_frame,
            text="Simulation Result",
            font=("Arial", 12, "bold"),
            bg="#f0f4f8",
            padx=10,
            pady=10
        )
        result_frame.pack(fill="x", pady=5)

        self.result_label = tk.Label(
            result_frame,
            text="Add edges or load the example graph to begin.",
            font=("Arial", 12),
            bg="#f0f4f8",
            fg="#17365D",
            justify="left",
            wraplength=760
        )
        self.result_label.pack(anchor="w")

    def add_edge(self):
        source = self.source_entry.get().strip()
        destination = self.destination_entry.get().strip()
        distance_text = self.distance_entry.get().strip()

        if not source or not destination or not distance_text:
            messagebox.showerror(
                "Input Error",
                "Please enter source, destination, and distance."
            )
            return

        if source == destination:
            messagebox.showerror(
                "Input Error",
                "Source and destination must be different."
            )
            return

        try:
            distance = float(distance_text)
            if not distance >= 0 or distance == float("inf"):
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Distance must be a finite, non-negative number."
            )
            return

        self.graph.setdefault(source, {})
        self.graph.setdefault(destination, {})

        # Treat each edge as an undirected connection.
        self.graph[source][destination] = distance
        self.graph[destination][source] = distance

        self.update_graph_display()
        self.update_node_options()

        self.source_entry.delete(0, tk.END)
        self.destination_entry.delete(0, tk.END)
        self.distance_entry.delete(0, tk.END)

    def load_example(self):
        self.graph = {
            "A": {"B": 4, "C": 2},
            "B": {"A": 4, "C": 1, "D": 5},
            "C": {"A": 2, "B": 1, "D": 8, "E": 10},
            "D": {"B": 5, "C": 8, "E": 2, "F": 6},
            "E": {"C": 10, "D": 2, "F": 3},
            "F": {"D": 6, "E": 3}
        }

        self.update_graph_display()
        self.update_node_options()

        self.result_label.config(
            text="Example graph loaded. Select a start and end node."
        )

    def clear_graph(self):
        self.graph.clear()
        self.graph_display.delete("1.0", tk.END)
        self.start_combo["values"] = []
        self.end_combo["values"] = []
        self.start_combo.set("")
        self.end_combo.set("")
        self.result_label.config(text="Graph cleared.")

    def update_graph_display(self):
        self.graph_display.delete("1.0", tk.END)

        for node in sorted(self.graph):
            connections = ", ".join(
                f"{neighbor} ({distance:g})"
                for neighbor, distance in sorted(
                    self.graph[node].items()
                )
            )
            self.graph_display.insert(
                tk.END, f"{node} -> {connections}\n"
            )

    def update_node_options(self):
        nodes = sorted(self.graph.keys())

        self.start_combo["values"] = nodes
        self.end_combo["values"] = nodes

        if nodes:
            if self.start_combo.get() not in nodes:
                self.start_combo.set(nodes[0])

            if self.end_combo.get() not in nodes:
                self.end_combo.set(nodes[-1])

    def dijkstra(self, start, end):
        distances = {node: float("inf") for node in self.graph}
        previous = {node: None for node in self.graph}

        distances[start] = 0
        priority_queue = [(0, start)]
        visited = []

        while priority_queue:
            current_distance, current_node = heapq.heappop(
                priority_queue
            )

            if current_distance != distances[current_node]:
                continue

            visited.append(current_node)

            if current_node == end:
                break

            for neighbor, weight in self.graph[current_node].items():
                new_distance = current_distance + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node

                    heapq.heappush(
                        priority_queue,
                        (new_distance, neighbor)
                    )

        if distances[end] == float("inf"):
            return None, float("inf"), visited

        path = []
        current = end

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        return path, distances[end], visited

    def find_shortest_path(self):
        start = self.start_combo.get()
        end = self.end_combo.get()

        if not self.graph:
            messagebox.showwarning(
                "Warning", "Please add edges or load the example graph."
            )
            return

        if not start or not end:
            messagebox.showwarning(
                "Warning", "Please select start and end nodes."
            )
            return

        path, distance, visited = self.dijkstra(start, end)

        if path is None:
            self.result_label.config(
                text=f"No path exists between {start} and {end}."
            )
            return

        path_text = " -> ".join(path)

        self.result_label.config(
            text=(
                f"Shortest Path: {path_text}\n"
                f"Total Distance: {distance:g}\n"
                f"Visited Nodes: {', '.join(visited)}\n"
                f"Algorithm: Dijkstra's Algorithm"
            )
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ShortestPathSimulator(root)
    root.mainloop()
