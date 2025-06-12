import sys

def load_pagerank(file_path):
    pr_dict = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                node = parts[0]
                try:
                    pr = float(parts[1])
                    pr_dict[node] = pr
                except ValueError:
                    continue
    return pr_dict

def check_convergence(file1, file2, epsilon=1e-4):
    pr1 = load_pagerank(file1)
    pr2 = load_pagerank(file2)

    all_nodes = set(pr1.keys()).union(set(pr2.keys()))
    max_diff = 0.0

    for node in all_nodes:
        val1 = pr1.get(node, 0.0)
        val2 = pr2.get(node, 0.0)
        diff = abs(val1 - val2)
        max_diff = max(max_diff, diff)
        print(f"{node}: |{val1:.6f} - {val2:.6f}| = {diff:.6f}")

    print("\nMax difference:", max_diff)
    if max_diff < epsilon:
        print("\n ĐÃ HỘI TỤ với epsilon =", epsilon)
        return True
    else:
        print("\n CHƯA HỘI TỤ với epsilon =", epsilon)
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Cách dùng: python check_converged.py resultX.txt resultY.txt")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    check_convergence(file1, file2)
