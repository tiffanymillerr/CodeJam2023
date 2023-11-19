// ignore_for_file: prefer_const_literals_to_create_immutables, prefer_const_constructors

import 'package:flutter/material.dart';

import '../pages/load_page.dart';

class TruckCard extends StatelessWidget {
  final int id;
  final String truck;
  final String equipType;
  final String length;
  final String time;

  const TruckCard({
    super.key,
    required this.truck,
    required this.id,
    required this.equipType,
    required this.length,
    required this.time,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 25),
      child: TextButton(
        onPressed: () {
          Navigator.push(
              context,
              MaterialPageRoute(
                  builder: (context) => LoadPage(
                        truckID: id,
                      )));
        },
        child: Container(
          height: 200,
          decoration: BoxDecoration(
            color: Colors.grey.shade100
            borderRadius: BorderRadius.circular(15),
          ),
          child: Column(
            children: [
              SizedBox(
                height: 25,
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 50),
                child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(truck, style: TextStyle(fontSize: 48)),
                      Text(id.toString(), style: TextStyle(fontSize: 48))
                    ]),
              ),
              SizedBox(
                height: 25,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  _ActionButton(text: equipType, type: 'Equipment'),
                  _ActionButton(text: length, type: 'Trips'),
                  _ActionButton(text: time, type: 'Time')
                ],
              )
            ],
          ),
        ),
      ),
    );
  }
}

class _ActionButton extends StatelessWidget {
  final String text;
  final String type;
  const _ActionButton({required this.text, required this.type});

  @override
  Widget build(BuildContext context) {
    String displayText = type == 'Equipment' && text.length > 10 ? 'Equip.' : text;
    
    return TextButton(
      style: ButtonStyle(
          minimumSize: MaterialStateProperty.all(Size(100, 75)),
          foregroundColor:
              MaterialStateProperty.all<Color>(Colors.grey.shade700),
          backgroundColor:
              MaterialStateProperty.all<Color>(Colors.lightGreen.shade100),
          shape: MaterialStateProperty.all<OutlinedBorder>(
            RoundedRectangleBorder(
                side: BorderSide.none,
                borderRadius: BorderRadius.horizontal(
                  left: Radius.circular(30),
                  right: Radius.circular(30),
                )),
          )),
      child: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Text('$type: $displayText', style: TextStyle(fontSize: 36), overflow: TextOverflow.ellipsis)),
      ),
      onPressed: () {},
    );
  }
}
