# Routing Algorithm

## Goal

Select the best gateway for every transaction.

## Factors

### Success Rate

Higher success rates receive higher scores.

### Latency

Lower response times receive higher scores.

### Gateway Health

Healthy gateways receive routing preference.

### Cost

Lower transaction costs improve scores.

### Payment Method Compatibility

Gateways supporting the requested payment method are prioritized.

## Routing Formula

Gateway Score =
(Success Rate Weight)
+
(Latency Weight)
+
(Health Weight)
+
(Cost Weight)
+
(Payment Method Weight)

The gateway with the highest score is selected.

## Failover

If the selected gateway fails, the router immediately attempts the next highest-ranked gateway.
