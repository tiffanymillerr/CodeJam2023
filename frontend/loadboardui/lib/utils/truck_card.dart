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
      padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 10),
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
          height: 100,
          decoration: BoxDecoration(color: Colors.grey.shade100),
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
                      //Text(truck, style: TextStyle(fontSize: 24)),
                      Text('ID: ${id.toString()}',
                          style: TextStyle(fontSize: 24)),
                      _ActionButton(text: equipType, type: 'Equipment'),
                      _ActionButton(text: length, type: 'Trips'),
                      _ActionButton(text: time, type: 'Time'),
                    ]),
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
    return TextButton(
      style: ButtonStyle(
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
        padding: const EdgeInsets.all(5.0),
        child: Text('$type: $text', style: TextStyle(fontSize: 24)),
      ),
      onPressed: () {},
    );
  }
}
