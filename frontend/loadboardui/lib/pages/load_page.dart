// ignore_for_file: prefer_const_constructors
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';

import '../utils/load_card.dart';
import '../utils/truck_card.dart';

class LoadPage extends StatefulWidget {
  final int truckID;

  const LoadPage({super.key, required this.truckID});

  @override
  State<LoadPage> createState() => _LoadPageState(truckID: truckID);
}

class _LoadPageState extends State<LoadPage> {
  final int truckID;

  _LoadPageState({required this.truckID});

  Future<List<LoadCard>?> updateIDs() async {
    final response = await http
        .get(Uri.parse('http://192.168.56.1/truck/$truckID/notifications'));

    List<LoadCard> cards = [];

    if (response.body != 'null' && response.statusCode == 200) {
      // If server returns an OK response, parse the JSON

      List<dynamic> jsonData = json.decode(response.body);

      // Iterate over the entries in the list
      jsonData.forEach((entry) {
        // Assuming each entry is a Map, you can iterate over its key-value pairs
        if (entry is Map<String, dynamic>) {
          cards.add(LoadCard(
              id: entry['id'],
              profit: entry['profit'],
              distance: entry['distance'],
              time: entry['time']));
        }
      });
      cards.sort((a, b) => a.id.compareTo(b.id));
      return cards;
    } else {
      // If the server did not return a 200 OK response,
      // throw an exception.
      print('Failed to load data');
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: () async {
        setState(() {});
      },
      child: FutureBuilder(
          future: updateIDs(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              // While waiting for the future to complete, show a loading indicator
              return CircularProgressIndicator();
            } else if (snapshot.hasError) {
              // If there's an error, display an error message
              return Text('Error: ${snapshot.error}');
            } else {
              // Once the future is complete, display the result
              return Scaffold(
                  backgroundColor: Colors.grey.shade300,
                  appBar: AppBar(
                      backgroundColor: Colors.grey.shade100,
                      centerTitle: true,
                      title: Text('Freight Elite',
                          style: TextStyle(
                              color: Colors.grey.shade700, fontSize: 36))),
                  body: Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: CustomScrollView(slivers: [
                      SliverAppBar(
                          pinned: true,
                          elevation: 4,
                          expandedHeight: 50,
                          backgroundColor: Colors.grey.shade300,
                          foregroundColor: Colors.grey.shade800,
                          title: Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: Text('Back',
                                style: TextStyle(color: Colors.grey.shade800)),
                          )),
                      SliverList(
                          delegate: SliverChildListDelegate(snapshot.data ??
                              [
                                Center(
                                    child: Text('No Load Notifications',
                                        style: TextStyle(fontSize: 36)))
                              ])),
                    ]),
                  ));
            }
          }),
    );
  }
}
