var data = [
  {
    label: "Product A",
    data: 10
  },
  {
    label: "Product B",
    data: 20
  },
  {
    label: "Product C",
    data: 30
  }
];

var options = {
  type: 'bar',
  data: {
    labels: data.map(function(d) {
      return d.label;
    }),
    datasets: [
      {
        backgroundColor: ['#3e95cd', '#8e5ea2', '#3cba9f'],
        data: data.map(function(d) {
          return d.data;
        })
      }
    ]
  },
  options: {
    legend: { display: false },
    title: {
      display: true,
      text: 'Most Moving Products'
    }
  }
};

var chart = new Chart(document.getElementById('chart'), options);