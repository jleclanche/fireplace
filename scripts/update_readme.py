"""
This script should replace the table
containing the implementation percentages
in README.md
"""
import sys
if __name__ == "__main__":
	sys.path.append("..")
import re
import implemented

README_PATH = "../README.md"

def main():
	with open(README_PATH) as f:
		content = f.read()

	table_regex = re.compile("<target>([\s\S]*)<\/target>")

	card_sets, standard_percentage = implemented.main()

	header = "### State Of Implementation ({:.1f}% of Standard Card Sets)\n\n".format(standard_percentage)
	table_start = "| Card Set      | Implemented |       |\n| ------------- |    :---:    | :---: |\n"

	new_table = "<target>\n\n" + header + table_start

	for card_set_name, impl, unimpl in card_sets:
		table_row = (
			"| **{}** | {}/{} | **{:.1f}%**\n"
			.format(card_set_name, impl, impl+unimpl, 100 * impl / (impl + unimpl))
		)
		new_table += table_row

	new_table += "\n\n</target>"

	with open(README_PATH, "w") as f:
		f.write(re.sub(table_regex, new_table, content))

if __name__ == '__main__':
	main()
