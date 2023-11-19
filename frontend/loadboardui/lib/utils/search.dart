// ignore_for_file: curly_braces_in_flow_control_structures

import 'dart:ffi';

import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

import '../pages/load_page.dart';

class AsyncSearchAnchor extends StatefulWidget {
  const AsyncSearchAnchor({super.key});

  @override
  State<AsyncSearchAnchor> createState() => AsyncSearchAnchorState();
}

class AsyncSearchAnchorState extends State<AsyncSearchAnchor> {
  // The query currently being searched for. If null, there is no pending
  // request.
  String? _searchingWithQuery;

  // The most recent options received from the API.
  late Iterable<Widget> _lastOptions = <Widget>[];

  final SearchController controller = SearchController();

  @override
  Widget build(BuildContext context) {
    return SearchAnchor(
        searchController: controller,
        builder: (BuildContext context, SearchController controller) {
          return SearchBar(
            controller: controller,
            padding: const MaterialStatePropertyAll<EdgeInsets>(
                EdgeInsets.symmetric(horizontal: 16.0)),
            onSubmitted: (value) {
              if (value.isNotEmpty)
                Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (context) =>
                            LoadPage(truckID: int.tryParse(value) ?? 0)));
            },
            hintText: 'Search Driver by ID',
            leading: const Icon(Icons.search),
          );
        },
        suggestionsBuilder:
            (BuildContext context, SearchController controller) async {
          _searchingWithQuery = controller.text;
          final response = (await http.get(Uri.parse(
              'http://192.168.56.1/truck'))); // Using IP for testing purposes, need to dynamically specify it
          print(response.body);
          final List<int> options = List<int>.from(json.decode(response.body));
          print(options);

          // If another search happened after this one, throw away these options.
          // Use the previous options instead and wait for the newer request to
          // finish.
          if (_searchingWithQuery != controller.text) {
            return _lastOptions;
          }

          _lastOptions = List<ListTile>.generate(options.length, (int index) {
            final int item = options[index];
            return ListTile(
              title: Text(item.toString()),
            );
          });

          return _lastOptions;
        });
  }
}
