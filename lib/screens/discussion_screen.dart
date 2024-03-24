import 'package:flutter/material.dart';
import 'pill.dart';

class DiscussionPage extends StatefulWidget {
  final Pill pill;

  DiscussionPage({Key? key, required this.pill}) : super(key: key);

  @override
  _DiscussionPageState createState() => _DiscussionPageState();
}

class Comment {
  final String id;
  final String userName;
  final String text;
  final DateTime createdAt;

  Comment({
    required this.id,
    required this.userName,
    required this.text,
    required this.createdAt,
  });
}

class _DiscussionPageState extends State<DiscussionPage> {
  List<Comment> comments = [];
  final TextEditingController _commentController = TextEditingController();

  @override
  void initState() {
    super.initState();
    fetchComments();
  }

  fetchComments() async {
    // API call to fetch comments based on widget.pill.id
    // Update `comments` list and call setState to refresh UI
  }

  postComment() async {
    // API call to post the comment
    // Then fetch comments again or append the new comment to the `comments` list and refresh UI
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white, // Set background color to white
      appBar: AppBar(
        title: Text('${widget.pill.name} Discussion',
            style: TextStyle(color: Color(0xFF0A84FF))),
        backgroundColor: Colors.white,
        iconTheme: IconThemeData(color: Color(0xFF0A84FF)),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: comments.length,
              itemBuilder: (context, index) {
                final comment = comments[index];
                return ListTile(
                  title: Text(comment.userName,
                      style: TextStyle(color: Color(0xFF0A84FF))),
                  subtitle: Text(comment.text),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: TextField(
              controller: _commentController,
              cursorColor:
                  Color(0xFF0A84FF), // Set cursor color to match the app theme
              decoration: InputDecoration(
                labelText: 'Add a comment...',
                labelStyle: TextStyle(color: Color(0xFF0A84FF)),
                suffixIcon: IconButton(
                  icon: Icon(Icons.send, color: Color(0xFF0A84FF)),
                  onPressed: postComment,
                ),
                enabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Color(0xFF0A84FF)),
                ),
                focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Color(0xFF0A84FF)),
                ),
              ),
            ),
          ),
        ],
      ),
      bottomNavigationBar: Padding(
        padding: EdgeInsets.only(bottom: 35.0), // Add padding at the bottom
        child: SizedBox(),
      ),
    );
  }
}
