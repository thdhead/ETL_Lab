import pandas as pd

CSV_PATH = r"caminho p/seu etl_lab_in"
OUT_XLSX = r"caminho p/seu etl_lab_out"

# EXTRACT
df = pd.read_csv(CSV_PATH)
df.columns = [c.strip() for c in df.columns]

# TRANSFORM
df["payment_due_date"] = pd.to_datetime(df["payment_due_date"], errors="coerce")
df["payment_received_date"] = pd.to_datetime(df["payment_received_date"], errors="coerce")

# True = pago até a data de vencimento; False = não pago ou pago após o vencimento
df["payment_received"] = df["payment_received_date"].notna() & (df["payment_received_date"] <= df["payment_due_date"])

def make_message(r):
    if r["payment_received"]:
        return f"Olá, {r['first_name']}! Pagamento recebido. Parabéns por manter seu empréstimo em dia!"
    else:
        due = r["payment_due_date"].strftime("%d/%m/%Y") if pd.notna(r["payment_due_date"]) else "N/D"
        return f"Olá, {r['first_name']}! Seu pagamento de R$ {r['payment_amount']:.2f} está pendente (venc. {due}). Regularize assim que possível."

df["message"] = df.apply(make_message, axis=1)

# LOAD
df.to_excel(OUT_XLSX, index=False)
print("Saved:", OUT_XLSX)