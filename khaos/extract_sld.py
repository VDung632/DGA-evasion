import tldextract
import sys

def remove_duplicates(input_list):
	seen = set()
	result = []
	for item in input_list:
		if item not in seen:
			seen.add(item)
			result.append(item)
	return result

def main():
	if len(sys.argv) < 3:
		raise Exception("Usage: python3 FULL_DOMAIN_FILE OUTPUT_FILE")

	domain_file = sys.argv[1]
	output_file = sys.argv[2]
	
	with open(domain_file, 'r') as f:
		domain_list = f.readlines()
	
	slds = [tldextract.extract(d).domain for d in domain_list]
	unique_slds = remove_duplicates(slds)

	for i in range(len(unique_slds)):
		unique_slds[i] += '\n'
	unique_slds[-1] = unique_slds[-1].strip()
	
	with open(output_file, 'w') as f:
		f.writelines(unique_slds)


if __name__ == "__main__":
	main()