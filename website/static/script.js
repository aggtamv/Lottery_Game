document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function () {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500); // Match with CSS transition duration
        });
    }, 5000);

    // Close button functionality
    document.querySelectorAll('.close').forEach(button => {
        button.addEventListener('click', function () {
            const alert = this.parentElement;
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500); // Match with CSS transition duration
        });
    });

    const buttonGrid = document.getElementById('button-grid');
    if (buttonGrid) {
        const container = document.querySelector('.buttons_container');
        const selectedNumbersSpan = document.getElementById('selectedNumbers');
        const submitBtn = document.getElementById('submitBtn');
        const resetBtn = document.getElementById('resetBtn');
        const drawBtn = document.getElementById('drawBtn');
        const lotteryDivs = document.querySelectorAll('.lotteryNumber');
        let selectedNumbers = [];
        let selectionConfirm = false;

        // Create number buttons dynamically
        for (let i = 1; i <= 30; i++) {
            const button = document.createElement('button');
            button.textContent = i;
            button.classList.add('btnNumbers');
            button.addEventListener('click', function() {
                if (selectedNumbers.length < 5 || button.classList.contains('selected')) {
                    button.classList.toggle('selected');
                    const number = parseInt(button.textContent);
                    if (button.classList.contains('selected')) {
                        if (!selectedNumbers.includes(number)) {
                            selectedNumbers.push(number);
                        }
                    } else {
                        selectedNumbers = selectedNumbers.filter(n => n !== number);
                    }
                    updateSelectedNumbersDisplay();
                }
            });
            container.appendChild(button);
        }

        function updateSelectedNumbersDisplay() {
            selectedNumbersSpan.textContent = selectedNumbers.join(', ');
        }

        submitBtn.addEventListener('click', function() {
            if (selectedNumbers.length === 5) {
                alert('Selection confirmed: ' + selectedNumbers.join(', '));
                selectionConfirm = true;
            } else {
                alert('Please select exactly 5 numbers.');
            }
        });

        resetBtn.addEventListener('click', function() {
            selectedNumbers = [];
            updateSelectedNumbersDisplay();
            selectionConfirm = false;
            document.querySelectorAll('.selected').forEach(button => {
                button.classList.remove('selected');
            });
            lotteryDivs.forEach(div => {
                div.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
                div.textContent = '';
            });
        });

        drawBtn.addEventListener('click', function(event) {
            event.preventDefault();
            if (selectedNumbers.length === 5 && selectionConfirm) {
                function getRandomInt(min, max) {
                    return Math.floor(Math.random() * (max - min + 1)) + min;
                }

                const randomNumbers = [];
                while (randomNumbers.length < 5) {
                    const randomNumber = getRandomInt(1, 30);
                    if (!randomNumbers.includes(randomNumber)) {
                        randomNumbers.push(randomNumber);
                    }
                }

                lotteryDivs.forEach((div, index) => {
                    const delay = index * 1000;
                    const number = randomNumbers[index];
                    setTimeout(() => {
                        div.textContent = number;
                        if (selectedNumbers.includes(number)) {
                            div.style.backgroundColor = 'green';
                        } else {
                            div.style.backgroundColor = 'red';
                        }
                    }, delay);
                });

                // Set hidden input values
                document.getElementById('selected_numbers').value = selectedNumbers.join(',');
                document.getElementById('lottery_numbers').value = randomNumbers.join(',');

                // Delay form submission to allow display of numbers
                setTimeout(() => {
                    document.getElementById('drawForm').submit();
                }, 5000); // Adjust delay to match the display time
            } else {
                alert('Please submit your guess first.');
            }
        });
    }
});
