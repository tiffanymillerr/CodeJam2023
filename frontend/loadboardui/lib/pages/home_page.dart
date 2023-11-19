// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import '../utils/search.dart';
import '../utils/truck_card.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List<int> truckIDs = [];

  Future<void> updateIDs() async {
    final response = await http.get(Uri.parse('http://localhost/truck'));

    if (response.statusCode == 200) {
      // If server returns an OK response, parse the JSON
      truckIDs = json.decode(response.body)['ids'];
    } else {
      // If the server did not return a 200 OK response,
      // throw an exception.
      throw Exception('Failed to load data');
    }
  }

  @override
  Widget build(BuildContext context) {
    // updateIDs();
    return Scaffold(
        backgroundColor: Colors.grey.shade300,
        appBar: AppBar(
            backgroundColor: Colors.grey.shade100,
            centerTitle: true,
            title: Text('Freight Elite',
                style: TextStyle(color: Colors.grey.shade700, fontSize: 36))),
        body: Padding(
          padding: const EdgeInsets.all(8.0),
          child: CustomScrollView(slivers: [
            SliverAppBar(
                pinned: true,
                elevation: 4,
                expandedHeight: 50,
                backgroundColor: Colors.grey.shade300,
                title: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: AsyncSearchAnchor(),
                )),
            SliverList(
                delegate: SliverChildListDelegate([
              TruckCard(
                  truck: 'Truck 1',
                  id: 12341,
                  equipType: 'Van',
                  length: 'Short'),
              TruckCard(
                  truck: 'Truck 1',
                  id: 12341,
                  equipType: 'Van',
                  length: 'Short'),
              TruckCard(
                  truck: 'Truck 1',
                  id: 12341,
                  equipType: 'Van',
                  length: 'Short'),
              TruckCard(
                  truck: 'Truck 1',
                  id: 12341,
                  equipType: 'Van',
                  length: 'Short'),
              TruckCard(
                  truck: 'Truck 1',
                  id: 12341,
                  equipType: 'Van',
                  length: 'Short')
            ])),
          ]),
        )

        // Column(children: [
        //   AsyncSearchAnchor(),
        //   Column(
        //     children: [
        //       TruckCard(
        //           truck: 'Truck 1',
        //           id: 12341,
        //           equipType: 'Van',
        //           length: 'Short'),
        //     ],
        //   )
        // ])
        );
  }
}
