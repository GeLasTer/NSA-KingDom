import json
from user import User
from graph import Graph

class JSONLoader:

    @staticmethod
    def load_from_file(filepath):
    
        # =====================================================
        # Read file
        # =====================================================
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filepath} not found!")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format!")

        # =====================================================
        # Initial validation
        # =====================================================
        if 'users' not in data or 'relations' not in data:
            raise ValueError("Dataset must contain 'users' and 'relations' keys!")

        if not isinstance(data['users'], list) or not isinstance(data['relations'], list):
            raise ValueError("'users' and 'relations' must be lists!")

        # =====================================================
        # Create empty graph
        # =====================================================
        graph = Graph()

        # =====================================================
        # Build User objects and add to graph
        # =====================================================
        for user_data in data['users']:
            user = User.from_dict(user_data)
            graph.add_user(user)

        # =====================================================
        # Build edges (relationships)
        # =====================================================
        for relation in data['relations']:
            user_id1, user_id2 = relation

            # =====================================================
            # Validate edge correctness
            # =====================================================
            if user_id1 == user_id2:
                continue

            user1_exists = False
            user2_exists = False

            if hasattr(graph, 'has_user'):
                user1_exists = graph.has_user(user_id1)
                user2_exists = graph.has_user(user_id2)
            else:
                user1_exists = graph.get_user(user_id1) is not None
                user2_exists = graph.get_user(user_id2) is not None

            # =====================================================
            # Add edge to graph
            # =====================================================
            if user1_exists and user2_exists:
                graph.add_edge(user_id1, user_id2)


        # =====================================================
        # Return the constructed graph
        # =====================================================
        return graph

    # =====================================================
    # Magic Methods
    # =====================================================

    def __repr__(self):
       
        return f"JSONLoader()"

    def __str__(self):
      
        return "JSONLoader for NSA Kingdom Project"

# =====================================================
# Test Section
# =====================================================
if __name__ == "__main__":
    try:
        graph = JSONLoader.load_from_file("dataset.json")
        print("Graph created successfully!")
        print(f"Total users: {graph.node_count()}")
        print(f"Total relationships: {graph.edge_count()}")
    except Exception as e:
        print(f"Error: {e}")

        