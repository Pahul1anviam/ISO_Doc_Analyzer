from agents.iso_agent import analyze_iso_from_pdf
import json

if __name__ == "__main__":
    file_path = "data/sample.pdf"  
    result = analyze_iso_from_pdf(file_path)

    with open("outputs/output.json", "w") as f:
        json.dump(result, f, indent=2)

    print("Analysis complete. Check outputs/output.json")
