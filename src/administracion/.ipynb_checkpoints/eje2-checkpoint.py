r = 0.01
monthly_cost = 1000.0
payment_12_original = 14000.0

def pv(amount, month, r=r):
    """Valor presente de 'amount' ocurrido en 'month' (meses desde inicio)."""
    return amount / ((1 + r) ** month)

def pv_costs(months, monthly=monthly_cost, r=r):
    """PV de una serie de costos mensuales pagados al final de cada mes (1..months)."""
    return sum(monthly / ((1 + r) ** t) for t in range(1, months + 1))

# Valores de referencia
pv_payment_12_original = pv(payment_12_original, 12)
pv_costs_12 = pv_costs(12)
npv_orig = pv_payment_12_original - pv_costs_12

pv_costs_6 = pv_costs(6)

# a) Pago en mes 14 (sin costos adicionales). X tal que PV(X en 14) = PV_pago_orig
#    => X = PV_pago_orig * (1+r)^14
X = pv_payment_12_original * ((1 + r) ** 14)

# Simplificación numérica: como PV_pago_orig = 14000 / (1+r)^12 -> X = 14000 * (1+r)^2
X_simplified = payment_12_original * ((1 + r) ** 2)

# b) Entrega en mes 6, pago en mes 12. Buscar Y tal que:
#    PV(Y en 12) - PV_costos_6 = NPV_orig  =>  Y = (NPV_orig + PV_costos_6) * (1+r)^12
Y = (npv_orig + pv_costs_6) * ((1 + r) ** 12)

# c) Entrega en mes 6, pago en mes 6. Buscar Z tal que:
#    PV(Z en 6) - PV_costos_6 = NPV_orig  =>  Z = (NPV_orig + PV_costos_6) * (1+r)^6
Z = (npv_orig + pv_costs_6) * ((1 + r) ** 6)

# Mostrar resultados con formato
print("Parámetros:")
print(f"  costo mensual = ${monthly_cost:.2f}, tasa mensual = {r*100:.2f}%, pago original = ${payment_12_original:.2f} en mes 12\n")

print("Referencias:")
print(f"  PV(pago original en mes 12) = ${pv_payment_12_original:,.2f}")
print(f"  PV(costos 12 meses) = ${pv_costs_12:,.2f}")
print(f"  NPV original (proveedor) = PV(pago) - PV(costos) = ${npv_orig:,.2f}\n")

print("a) Pago en mes 14 (dos meses después), sin costos adicionales:")
print("   Fórmula: X = PV_pago_orig * (1+r)^14")
print(f"   Simplificación: X = 14000 * (1+r)^2 = ${X_simplified:,.2f}")
print(f"   (cálculo directo) X = ${X:,.2f}\n")

print("b) Entrega mes 6, pago en mes 12 (mantienen pago a mes 12):")
print("   Fórmula: Y = (NPV_orig + PV_costos_6) * (1+r)^12")
print(f"   PV(costos 6 meses) = ${pv_costs_6:,.2f}")
print(f"   Resultado: Y = ${Y:,.2f}  (monto a pagar en mes 12)\n")

print("c) Entrega y pago en mes 6:")
print("   Fórmula: Z = (NPV_orig + PV_costos_6) * (1+r)^6")
print(f"   Resultado: Z = ${Z:,.2f}  (monto a pagar en mes 6)\n")

print("Notas:")
print("- Todas las fórmulas usadas están en valor presente respecto al inicio (mes 0).")
print("- Para que el cambio sea neutro se mantiene la misma utilidad NPV que bajo el contrato original.")

STDOUT/STDERR
Parámetros:
  costo mensual = $1000.00, tasa mensual = 1.00%, pago original = $14000.00 en mes 12

Referencias:
  PV(pago original en mes 12) = $12,424.29
  PV(costos 12 meses) = $11,255.08
  NPV original (proveedor) = PV(pago) - PV(costos) = $1,169.21

a) Pago en mes 14 (dos meses después), sin costos adicionales:
   Fórmula: X = PV_pago_orig * (1+r)^14
   Simplificación: X = 14000 * (1+r)^2 = $14,281.40
   (cálculo directo) X = $14,281.40

b) Entrega mes 6, pago en mes 12 (mantienen pago a mes 12):
   Fórmula: Y = (NPV_orig + PV_costos_6) * (1+r)^12
   PV(costos 6 meses) = $5,795.48
   Resultado: Y = $7,847.98  (monto a pagar en mes 12)

c) Entrega y pago en mes 6:
   Fórmula: Z = (NPV_orig + PV_costos_6) * (1+r)^6
   Resultado: Z = $7,393.16  (monto a pagar en mes 6)

Notas:
- Todas las fórmulas usadas están en valor presente respecto al inicio (mes 0).
- Para que el cambio sea neutro se mantiene la misma utilidad NPV que ba