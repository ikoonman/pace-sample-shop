import { useEffect, useState } from "react";
import { fetchOrder, formatCents, OrderSummaryDto } from "../api/shopClient";

export function OrderSummary(props: { baseUrl: string; orderId: string }) {
  const [order, setOrder] = useState<OrderSummaryDto | null>(null);

  useEffect(() => {
    fetchOrder(props.baseUrl, props.orderId).then(setOrder);
  }, [props.baseUrl, props.orderId]);

  if (!order) {
    return <p>Loading…</p>;
  }
  return (
    <section>
      <h2>Order {order.id}</h2>
      <p>{order.status}: {formatCents(order.totalCents)}</p>
    </section>
  );
}
