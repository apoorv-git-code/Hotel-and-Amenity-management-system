# Hotel & Amenity Management System

A Streamlit application for managing hotels, rooms, amenities, customers, and bookings with MongoDB.

## Run locally

1. Use Python 3.12 and install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Set `MONGODB_URI` to a reachable MongoDB connection string. For a local MongoDB server, the app defaults to `mongodb://localhost:27017/`.

   ```powershell
   $env:MONGODB_URI = "mongodb+srv://<user>:<password>@<cluster>/<database>"
   ```

   Set `MONGODB_DATABASE` to override the default database name, `hotel_management`.

3. Start Streamlit:

   ```bash
   streamlit run app.py
   ```

   Or use `python main.py`; it listens on `PORT` when set and otherwise uses port `8501`.

## Deploy on Render

The app and its `render.yaml` deployment configuration are in the repository root.

1. Create a Render Blueprint from the repository and select the `main` branch.
2. When prompted, set the secret `MONGODB_URI` to your MongoDB Atlas connection string. Do not commit credentials.
3. Keep `MONGODB_DATABASE` as `hotel_management` unless your database uses another name.

Render builds with `pip install -r requirements.txt`, starts Streamlit on Render's assigned `$PORT`, and checks `/_stcore/health`.

## Performance notes

- MongoDB clients are shared across Streamlit sessions.
- Read-only collection results are cached for 30 seconds and cleared after successful writes.
- Hotel room data is loaded once per page instead of querying once per hotel.
- The interface uses local system fonts and CSS artwork instead of making external font or hotel-image requests.

## Project files

- `app.py`: Streamlit UI and page routing
- `database.py`: MongoDB configuration and shared client
- `auth.py`: User registration and login
- `hotel.py`, `room.py`, `amenities.py`, `customers.py`, `booking.py`: Collection operations
- `main.py`: Local Streamlit launcher
- `render.yaml` (repository root): Render Blueprint deployment configuration

## Tests

```bash
python -m unittest discover -s tests
```
