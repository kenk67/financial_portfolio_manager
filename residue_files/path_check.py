from pathlib import Path

current_dir = Path(__file__).parent
print(current_dir)

a = "testing testing"
name = "check"
file_path = current_dir / f"{name}.txt"
print(file_path)
file_path.write_text(a)
