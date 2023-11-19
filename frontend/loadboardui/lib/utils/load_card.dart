// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';

class LoadCard extends StatelessWidget {
  final int id;
  final int profit;
  final int distance;
  final String time;

  const LoadCard(
      {super.key,
      required this.id,
      required this.profit,
      required this.distance,
      required this.time});

  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 25),
        child: Container(
          height: 200,
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
                      Text('$distance Miles Away From You !',
                          style: TextStyle(fontSize: 24)),
                      Text(time.toString(),
                          style: TextStyle(
                              fontSize: 24, color: Colors.grey.shade500))
                    ]),
              ),
              SizedBox(
                height: 25,
              ),
              Text('Load available near your current location.'),
              Text('Load ID $id'),
              Text('\$$profit profit for entire trip')
            ],
          ),
        ));
  }
}
