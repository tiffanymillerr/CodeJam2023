// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

final fcur = NumberFormat("#,##0.00", "en_US");

class LoadCard extends StatelessWidget {
  final int id;
  final double profit;
  final double distance;
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
          decoration: BoxDecoration(
              color: Colors.grey.shade100, border: Border.all(width: 4)),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                SizedBox(
                  height: 10,
                ),
                Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text('${distance.toStringAsFixed(1)} miles away',
                          style: TextStyle(fontSize: 24)),
                      Text(time.toString(),
                          style: TextStyle(
                              fontSize: 24,
                              color: Colors.grey.shade500,
                              fontWeight: FontWeight.bold))
                    ]),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        Text('\$${fcur.format(profit)}',
                            style: TextStyle(fontSize: 48)),
                        Text(' (estimated profit)',
                            style: TextStyle(fontSize: 18))
                      ],
                    ),
                    Text(
                      'Load ID $id',
                      style: TextStyle(fontSize: 24),
                    )
                  ],
                ),
                SizedBox(
                  height: 5,
                ),
              ],
            ),
          ),
        ));
  }
}
