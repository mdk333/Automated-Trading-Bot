# Define the stop loss and take profit percentages
stop_loss_pct, take_profit_pct = 0.01, 0.02

def place_order(strategy, symbol, qty, side, typ, time_in_force, limit_price=None, stop_price=None):
    # Place an order
    order = api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type=typ,
        time_in_force=time_in_force,
        limit_price=limit_price,
        stop_price=stop_price
    )

    # Log the order to MongoDB
    db['orders'].insert_one(order._raw)

    # If it's a market order, also place a stop loss and a take profit order
    if typ == 'market':
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell' if side == 'buy' else 'buy',
            type='stop_limit',
            time_in_force='gtc',
            limit_price=order.filled_avg_price * (1 - stop_loss_pct) if side == 'buy' else order.filled_avg_price * (1 + stop_loss_pct),
            stop_price=order.filled_avg_price * (1 - stop_loss_pct) if side == 'buy' else order.filled_avg_price * (1 + stop_loss_pct),
        )
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell' if side == 'buy' else 'buy',
            type='limit',
            time_in_force='gtc',
            limit_price=order.filled_avg_price * (1 + take_profit_pct) if side == 'buy' else order.filled_avg_price * (1 - stop_loss_pct),
        )
