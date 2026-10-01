export interface OrderSummaryDto {
  id: string;
  status: string;
  totalCents: number;
}

export async function fetchOrder(baseUrl: string, orderId: string): Promise<OrderSummaryDto> {
  const res = await fetch(`${baseUrl}/orders/${encodeURIComponent(orderId)}`);
  if (!res.ok) {
    throw new Error(`order ${orderId}: HTTP ${res.status}`);
  }
  return (await res.json()) as OrderSummaryDto;
}

export function formatCents(cents: number, currency = "GBP"): string {
  const sign = cents < 0 ? "-" : "";
  const abs = Math.abs(cents);
  return `${sign}${currency} ${Math.floor(abs / 100)}.${String(abs % 100).padStart(2, "0")}`;
}
