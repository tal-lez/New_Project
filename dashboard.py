from pathlib import Path
import json

SAMPLE_DATA = {
    "companyName": "Data Insight Co.",
    "generatedAt": "2026-06-15",
    "summary": {
        "totalRevenue": 1264800,
        "orders": 9830,
        "newCustomers": 2450,
        "returningCustomers": 1580
    },
    "monthlyRevenue": {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "values": [175000, 183000, 198000, 210000, 225000, 249800]
    },
    "categoryBreakdown": {
        "labels": ["Analytics", "Consulting", "Training", "Support"],
        "values": [540000, 320000, 210000, 194800]
    },
    "customerSegments": {
        "labels": ["New", "Returning", "Referral", "Organic"],
        "values": [2450, 1580, 1130, 760]
    }
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{companyName} Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: #f4f7fb;
            margin: 0;
            color: #1f2937;
        }
        .page {
            width: min(1200px, 94vw);
            margin: 0 auto;
            padding: 32px 0 64px;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            flex-wrap: wrap;
            margin-bottom: 24px;
        }
        .title-group h1 {
            margin: 0;
            font-size: clamp(2rem, 2.5vw, 3rem);
        }
        .title-group p {
            margin: 0.5rem 0 0;
            color: #4b5563;
        }
        .grid {
            display: grid;
            gap: 24px;
        }
        .summary-grid {
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        }
        .card {
            background: #ffffff;
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 18px 50px rgba(15, 23, 42, 0.08);
        }
        .card h2 {
            margin: 0 0 8px;
            font-size: 0.9rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: #6b7280;
        }
        .value {
            font-size: 2.05rem;
            margin: 0;
            color: #111827;
        }
        .metric-note {
            margin: 12px 0 0;
            color: #4b5563;
            font-size: 0.95rem;
        }
        .charts {
            grid-template-columns: 2fr 1fr;
        }
        .chart-card {
            min-height: 380px;
        }
        .two-column {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 24px;
        }
        @media (max-width: 900px) {
            .charts,
            .two-column {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <main class="page">
        <section class="header">
            <div class="title-group">
                <h1>{companyName} Dashboard</h1>
                <p>Generated on {generatedAt}. This dashboard shows revenue, category mix, and customer segment trends.</p>
            </div>
        </section>

        <section class="grid summary-grid">
            <div class="card">
                <h2>Total Revenue</h2>
                <p class="value">${summary[totalRevenue]:,}</p>
                <p class="metric-note">Revenue across the last six months.</p>
            </div>
            <div class="card">
                <h2>Orders</h2>
                <p class="value">{summary[orders]:,}</p>
                <p class="metric-note">Total completed orders for the period.</p>
            </div>
            <div class="card">
                <h2>New Customers</h2>
                <p class="value">{summary[newCustomers]:,}</p>
                <p class="metric-note">Customers acquired in the current period.</p>
            </div>
            <div class="card">
                <h2>Returning Customers</h2>
                <p class="value">{summary[returningCustomers]:,}</p>
                <p class="metric-note">Repeat customers helping sustain growth.</p>
            </div>
        </section>

        <section class="grid charts" style="margin-top: 24px;">
            <div class="card chart-card">
                <h2>Monthly Revenue Trend</h2>
                <canvas id="revenueLine"></canvas>
            </div>
            <div class="two-column">
                <div class="card chart-card">
                    <h2>Category Revenue Mix</h2>
                    <canvas id="categoryPie"></canvas>
                </div>
                <div class="card chart-card">
                    <h2>Customer Segment Distribution</h2>
                    <canvas id="customerPie"></canvas>
                </div>
            </div>
        </section>
    </main>

    <script>
        const chartData = {json_data};

        const revenueLine = document.getElementById('revenueLine').getContext('2d');
        new Chart(revenueLine, {
            type: 'line',
            data: {
                labels: chartData.monthlyRevenue.labels,
                datasets: [{
                    label: 'Monthly Revenue',
                    data: chartData.monthlyRevenue.values,
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(59, 130, 246, 0.15)',
                    fill: true,
                    tension: 0.35,
                    pointRadius: 5,
                    pointBackgroundColor: '#1d4ed8'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        ticks: {
                            callback: value => '$' + Intl.NumberFormat().format(value)
                        },
                        grid: { color: 'rgba(148, 163, 184, 0.18)' }
                    },
                    x: {
                        grid: { color: 'rgba(148, 163, 184, 0.14)' }
                    }
                }
            }
        });

        const categoryPie = document.getElementById('categoryPie').getContext('2d');
        new Chart(categoryPie, {
            type: 'doughnut',
            data: {
                labels: chartData.categoryBreakdown.labels,
                datasets: [{
                    data: chartData.categoryBreakdown.values,
                    backgroundColor: ['#2563eb', '#9333ea', '#0f766e', '#dc2626']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });

        const customerPie = document.getElementById('customerPie').getContext('2d');
        new Chart(customerPie, {
            type: 'pie',
            data: {
                labels: chartData.customerSegments.labels,
                datasets: [{
                    data: chartData.customerSegments.values,
                    backgroundColor: ['#14b8a6', '#f59e0b', '#3b82f6', '#8b5cf6']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    </script>
</body>
</html>
"""


def build_dashboard(output_path: Path | str = 'dashboard.html') -> Path:
    output_path = Path(output_path)
    json_data = json.dumps(SAMPLE_DATA, indent=2)
    html = HTML_TEMPLATE.format(
        companyName=SAMPLE_DATA['companyName'],
        generatedAt=SAMPLE_DATA['generatedAt'],
        summary=SAMPLE_DATA['summary'],
        json_data=json_data
    )
    output_path.write_text(html, encoding='utf-8')
    return output_path


def main() -> None:
    dashboard_path = build_dashboard()
    print(f'Dashboard created: {dashboard_path.resolve()}')
    print('Open this file in a browser to view the dashboard.')


if __name__ == '__main__':
    main()
