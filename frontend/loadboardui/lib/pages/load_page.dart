// ignore_for_file: prefer_const_constructors
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';

import '../utils/load_card.dart';
import '../utils/truck_card.dart';

class LoadPage extends StatelessWidget {
  final int truckID;

  const LoadPage({super.key, required this.truckID});

  Future<void> updateIDs() async {
    final response = await http
        .get(Uri.parse('http://localhost/truck/$truckID/notifications'));

    if (response.statusCode == 200) {
      // If server returns an OK response, parse the JSON
      
      List<Object> data = json.decode(response.body);
      for ()
    } else {
      // If the server did not return a 200 OK response,
      // throw an exception.
      throw Exception('Failed to load data');
    }
  }

  @override
  Widget build(BuildContext context) {
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
                  child: Text('Here'),
                )),
            SliverList(
                delegate: SliverChildListDelegate([
              LoadCard(id: 9000, profit: 2400, distance: 500, time: '14:30'),
              LoadCard(id: 9000, profit: 2400, distance: 500, time: '14:30'),
              LoadCard(id: 9000, profit: 2400, distance: 500, time: '14:30'),
              LoadCard(id: 9000, profit: 2400, distance: 500, time: '14:30'),
            ])),
          ]),
        ));
  }
}
