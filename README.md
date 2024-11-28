# README

Links:
- https://pypi.org/project/ctrader-fix/
- https://github.com/spotware/cTraderFixPy
- https://github.com/spotware/cTraderFixPy/blob/main/samples/ConsoleSample/main.py
- https://chatgpt.com/c/673cf0a6-7bf4-800f-9112-d223cd582853

```sh
curl -X POST http://localhost:5001/order \
    -H "Content-Type: application/json" \
    -d '{
          "ClOrdID": "order123",
          "Symbol": 1,
          "Side": 1,
          "OrderQty": 1000,
          "OrdType": 10029
        }'
```

## message debugger
https://fixparser.targetcompid.com/

```sh
8=FIX.4.4|9=123|35=A|49=demo.icmarkets.9229960|56=cServer|57=TRADE|50=TRADE|34=1|52=20241120-13:47:05|98=0|108=30|553=9229960|554=EIWX0641|10=210|
8=FIX.4.4|9=98|35=x|49=demo.icmarkets.9229960|56=cServer|57=TRADE|50=TRADE|34=2|52=20241120-13:47:05|320=A|559=0|10=189|
8=FIX.4.4|9=163|35=D|49=demo.icmarkets.9229960|56=cServer|57=TRADE|50=TRADE|34=3|52=20241120-13:47:05|11=market_order_001|55=1|54=1|60=20241120-13:47:05|38=1000|40=1|494=From FIX|10=138|
8=FIX.4.4|9=164|35=D|49=demo.icmarkets.9229960|56=cServer|57=TRADE|50=TRADE|34=4|52=20241120-13:47:06|11=465709098|55=1|54=2|60=20241120-13:47:06|38=1000|40=2|44=1.2|721=465709098|10=246|
```