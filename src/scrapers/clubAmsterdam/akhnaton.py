import requests
import json
from datetime import datetime


def bot():
    url = "https://ra.co/graphql"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
    }

    current_time_iso = datetime.today().isoformat() + "Z"

    payload = {
        "operationName": "GET_EVENTS_LISTING",
        "variables": {
            "indices": ["EVENT"],
            "pageSize": 20,
            "page": 1,
            "aggregations": [],
            "filters": [
                {"type": "CLUB", "value": "2763"},
                {"type": "DATERANGE", "value": json.dumps({"gte": current_time_iso})},
                {"type": "YEAR", "value": "2025"}
            ],
            "sortOrder": "ASCENDING",
            "sortField": "DATE"
        },
        "query": """
        query GET_EVENTS_LISTING(
        $indices: [IndexType!],
        $aggregations: [ListingAggregationType!],
        $filters: [FilterInput],
        $pageSize: Int,
        $page: Int,
        $sortField: FilterSortFieldType,
        $sortOrder: FilterSortOrderType
        ) {
        listing(
            indices: $indices,
            aggregations: $aggregations,
            filters: $filters,
            pageSize: $pageSize,
            page: $page,
            sortField: $sortField,
            sortOrder: $sortOrder
        ) {
            data {
            ...eventFragment
            }
        }
        }

        fragment eventFragment on Event {
        id
        title
        date
        startTime
        contentUrl
        }
        """
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.ok:
        data = response.json()
        events = data.get("data", {}).get("listing", {}).get("data", [])
        formatted_events = []

        for event in events:
            date_str = event.get("date")
            time_str = event.get("startTime")
            title = event.get("title")
            url_path = event.get("contentUrl")

            formatted_events.append({
                'date': date_str.split('T')[0],
                'time': time_str.split('T')[1][:5],
                'title': title,
                'venue': "Akhnaton",
                'price': "",
                'site': "https://www.akhnaton.nl/",
                'address': "Nieuwezijds Kolk 25, 1012 PV Amsterdam"
            })

    return formatted_events

