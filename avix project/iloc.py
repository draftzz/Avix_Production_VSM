import pdfplumber
import re
import matplotlib.pyplot as plt

# Paths to all uploaded PDFs
pdf_files = {
    "FA0": "O:/avix padrão python/avix FA0.pdf",
    "FA1.1": "O:/avix padrão python/avix FA1.1.pdf",
    "FA1.2": "O:/avix padrão python/avix FA1.2.pdf",
    "FA2": "O:/avix padrão python/avix FA2.pdf",
    "FA3.1": "O:/avix padrão python/avix FA3.1.pdf",
    "FA3.2": "O:/avix padrão python/avix FA3.2.pdf",
    "FA4": "O:/avix padrão python/avix FA4.pdf",
    "FA5": "O:/avix padrão python/avix FA5.pdf",
}

# Regex pattern to extract "Tempo total: [number]"
pattern = re.compile(r"Tempo total:\s*([\d.]+)")

# Dictionary to store results
results = {}
overall_total = 0
overall_count = 0

# Process each PDF
for function, file_path in pdf_files.items():
    function_total = 0
    function_count = 0
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            matches = pattern.findall(text)
            for match in matches:
                try:
                    time_value = float(match)
                    function_total += time_value
                    function_count += 1
                except ValueError:
                    continue
    if function_count > 0:
        results[function] = {
            "total_time": function_total,
            "average_time": function_total / function_count,
            "count": function_count,
        }
        overall_total += function_total
        overall_count += function_count

# Calculate overall average
overall_average = overall_total / overall_count if overall_count > 0 else 0

# Print Results
print("Resultados por Função:")
for function, data in results.items():
    print(f"{function}: Total: {data['total_time']} s | Média: {data['average_time']:.2f} s | Contagem: {data['count']}")

#print(f"\nSoma Total dos Tempos: {overall_total} s")
#print(f"Total de Tempos Contados: {overall_count}")
print(f"Média Geral: {overall_average:.2f} s")

# Plotting
functions = list(results.keys())
averages = [data['average_time'] for data in results.values()]
totals = [data['total_time'] for data in results.values()]

# Bar Chart: Average Times by Function
plt.figure(figsize=(10, 6))
plt.bar(functions, averages, alpha=0.7)
plt.title('Média de Tempos por Função')
plt.ylabel('Tempo Médio (s)')
plt.xlabel('Função')
plt.show()

# Pie Chart: Total Times Contribution by Function
plt.figure(figsize=(8, 8))
plt.pie(totals, labels=functions, autopct='%1.1f%%', startangle=140)
plt.title('Contribuição Total dos Tempos por Função')
plt.show()
