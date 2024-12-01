// Полный список станций с координатами
const stations = [
    { name: "Парк Горького", lat: 55.73013, lon: 37.597184 },
    { name: "Нескучный сад", lat: 55.722427, lon: 37.590694 },
    { name: "Крымский мост", lat: 55.732427, lon: 37.596061 },
    { name: "Марьино", lat: 55.641785, lon: 37.725065 },
    { name: "Печатники", lat: 55.683699, lon: 37.714149 },
    { name: "Меловой", lat: 55.69106, lon: 37.696817 },
    { name: "Южный речной вокзал", lat: 55.689415, lon: 37.675846 },
    { name: "Кленовый бульвар", lat: 55.686457, lon: 37.67215 },
    { name: "Воробьевы горы", lat: 55.711738, lon: 37.546826 },
    { name: "Киевский", lat: 55.743672, lon: 37.571839 },
    { name: "Красный Октябрь", lat: 55.745129, lon: 37.610627 },
    { name: "Сити – Экспоцентр", lat: 55.748745, lon: 37.546796 },
    { name: "Новоспасский", lat: 55.730281, lon: 37.653392 },
    { name: "Китай-город", lat: 55.748462, lon: 37.635886 },
    { name: "Патриарший", lat: 55.743972, lon: 37.608138 },
    { name: "Лужники – Северный", lat: 55.726423, lon: 37.545615 },
    { name: "Третьяковский", lat: 55.744502, lon: 37.618414 },
    { name: "Кутузовский", lat: 55.744387, lon: 37.538187 },
    { name: "Троице-Лыково", lat: 55.79192, lon: 37.409289 },
    { name: "Парк Фили", lat: 55.749486, lon: 37.475581 },
    { name: "Захарково", lat: 55.849065, lon: 37.459077 },
    { name: "Трёхгорный", lat: 55.754254, lon: 37.56394 },
    { name: "Сити – Багратион", lat: 55.746481, lon: 37.545233 },
    { name: "Лужники - Центральный", lat: 55.713129, lon: 37.549501 },
    { name: "Северный речной вокзал", lat: 55.851125, lon: 37.466138 },
    { name: "Андреевский", lat: 55.711646, lon: 37.572238 },
    { name: "Зарядье", lat: 55.749528, lon: 37.629242 },
    { name: "Серебряный бор-2", lat: 55.785823, lon: 37.424496 },
    { name: "Серебряный бор-3", lat: 55.785127, lon: 37.444882 },
    { name: "Сити – Центральный", lat: 55.746589, lon: 37.541693 },
    { name: "Автозаводский мост", lat: 55.702836, lon: 37.626632 },
    { name: "Химки", lat: 55.886542, lon: 37.458891 },
    { name: "Сердце Столицы", lat: 55.760497, lon: 37.512246 },
    { name: "ЗИЛ", lat: 55.699935, lon: 37.628875 },
    { name: "Нагатинский затон", lat: 55.685878, lon: 37.701144 },
    { name: "Береговой", lat: 55.758389, lon: 37.512611 }
];
// Добавляем станции в выпадающие списки
const fromSelect = document.getElementById("from-station");
const toSelect = document.getElementById("to-station");
stations.forEach(station => {
    const optionFrom = document.createElement("option");
    optionFrom.value = station.name;
    optionFrom.textContent = station.name;
    fromSelect.appendChild(optionFrom);
    const optionTo = document.createElement("option");
    optionTo.value = station.name;
    optionTo.textContent = station.name;
    toSelect.appendChild(optionTo);
});

ymaps.ready(initMap);
function initMap() {
    const myMap = new ymaps.Map("map", {
        center: [55.7558, 37.6173],
        zoom: 11,
    });
    let userLocationMarker;
    let routeToStation = null; // Маршрут от пользователя до станции отправления
    let waterRouteLine = null; // Маршрут по воде
    const fromSelect = document.getElementById("from-station");
    // Отображение всех станций на карте
    stations.forEach(station => {
        const placemark = new ymaps.Placemark([station.lat, station.lon], {
            hintContent: station.name,
        }, {
            iconColor: '#0000FF',
        });
        myMap.geoObjects.add(placemark);
    });
    // Получение геолокации пользователя
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(position => {
            const userLat = position.coords.latitude;
            const userLon = position.coords.longitude;
            // Обновляем метку пользователя
            if (userLocationMarker) {
                myMap.geoObjects.remove(userLocationMarker);
            }
            userLocationMarker = new ymaps.Placemark([userLat, userLon], {
                hintContent: "Ваше местоположение",
            }, {
                iconColor: '#0095b6',
            });
            myMap.geoObjects.add(userLocationMarker);
            // Построение маршрута от пользователя до станции отправления
            updateRouteToStation(userLat, userLon, fromSelect.value);
        }, () => {
            alert('Не удалось получить ваше местоположение.');
        });
    } else {
        alert('Геолокация не поддерживается вашим браузером.');
    }
    // Функция обновления маршрута до станции отправления
    function updateRouteToStation(userLat, userLon, stationName) {
        if (!stationName) {
            // Если станция не выбрана, удаляем маршрут
            if (routeToStation) {
                myMap.geoObjects.remove(routeToStation);
                routeToStation = null;
            }
            return;
        }
        const selectedStation = stations.find(station => station.name === stationName);
        if (selectedStation) {
            // Удаляем предыдущий маршрут
            if (routeToStation) {
                myMap.geoObjects.remove(routeToStation);
            }
            // Создаем новый маршрут
            ymaps.route([[userLat, userLon], [selectedStation.lat, selectedStation.lon]])
                .then(route => {
                    routeToStation = route;
                    myMap.geoObjects.add(routeToStation);
                    // Расчет и отображение расстояния до станции
                    const distanceToStation = calculateDistance(userLat, userLon, selectedStation.lat, selectedStation.lon);
                    document.querySelector('.route-details').innerHTML = `
                        <div>Расстояние до станции отправления: ${distanceToStation.toFixed(2)} км</div>
                    `;
                });
        }
    }
    // Обработчик для обновления маршрута при изменении станции отправления
    fromSelect.addEventListener("change", () => {
        if (userLocationMarker) {
            const userCoords = userLocationMarker.geometry.getCoordinates();
            updateRouteToStation(userCoords[0], userCoords[1], fromSelect.value);
        }
    });
    // Обработчик для расчета водного маршрута
    document.getElementById("calculate-route").addEventListener("click", () => {
        const fromName = fromSelect.value;
        const toName = document.getElementById("to-station").value;
        if (!fromName || !toName || fromName === toName) {
            alert("Выберите разные станции");
            return;
        }
        const fromStation = stations.find(station => station.name === fromName);
        const toStation = stations.find(station => station.name === toName);
        if (fromStation && toStation) {
            // Удаляем предыдущий маршрут
            if (routeToStation) {
                myMap.geoObjects.remove(routeToStation);
                routeToStation = null;
            }
            // Удаляем старый водный маршрут
            if (waterRouteLine) {
                myMap.geoObjects.remove(waterRouteLine);
            }
            // Строим новый водный маршрут
            const midPoint = calculateArcPoint(fromStation.lat, fromStation.lon, toStation.lat, toStation.lon, 0.2);
            waterRouteLine = new ymaps.Polyline([
                [fromStation.lat, fromStation.lon],
                midPoint,
                [toStation.lat, toStation.lon],
            ], {}, {
                strokeColor: "#1E90FF",
                strokeWidth: 4,
                strokeOpacity: 0.8,
            });
            myMap.geoObjects.add(waterRouteLine);
            // Рассчет и отображение данных о маршруте
            const distance = calculateDistance(fromStation.lat, fromStation.lon, toStation.lat, toStation.lon);
            const time = distance / 15 * 60; // Скорость: 15 км/ч
            const cost = Math.round(distance * 100); // 100 руб./км
            document.querySelector('.route-details').innerHTML = `
                <div>Расстояние по воде: ${distance.toFixed(2)} км</div>
                <div>Время в пути: ${Math.round(time)} мин</div>
                <div>Стоимость: ${cost} руб.</div>
            `;
        }
    });
    // Функция расчета расстояния
    function calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // Радиус Земли в км
        const dLat = ((lat2 - lat1) * Math.PI) / 180;
        const dLon = ((lon2 - lon1) * Math.PI) / 180;
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos((lat1 * Math.PI) / 180) * Math.cos((lat2 * Math.PI) / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        return 2 * R * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    }
    // Функция вычисления контрольной точки для дуги
    function calculateArcPoint(lat1, lon1, lat2, lon2, offset) {
        const midLat = (lat1 + lat2) / 2;
        const midLon = (lon1 + lon2) / 2;
        const dx = lon2 - lon1;
        const dy = lat2 - lat1;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const arcOffset = (distance / 2) * offset;
        return [midLat + (dy / distance) * arcOffset, midLon + (dx / distance) * arcOffset];
    }
}
document.addEventListener('DOMContentLoaded', function() {
    const userMenuBtn = document.getElementById('user-menu-btn');
    const userMenu = document.getElementById('user-menu');
    const userMenuContainer = document.querySelector('.user-menu-container');
    // Обработчик для кнопки капитанов
    userMenuBtn.addEventListener('click', function() {
        userMenuContainer.classList.toggle('active');
    });
    // Закрытие меню при клике вне его области
    document.addEventListener('click', function(event) {
        if (!userMenuContainer.contains(event.target)) {
            userMenuContainer.classList.remove('active');
        }
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const partnerMenuBtn = document.getElementById('partner-menu-btn');
    const partnerMenu = document.getElementById('partner-menu');
    const partnerMenuContainer = document.querySelector('.partner-menu-container');
    // Обработчик для кнопки капитанов
    partnerMenuBtn.addEventListener('click', function() {
        partnerMenuContainer.classList.toggle('active');
    });
    // Закрытие меню при клике вне его области
    document.addEventListener('click', function(event) {
        if (!partnerMenuContainer.contains(event.target)) {
            partnerMenuContainer.classList.remove('active');
        }
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const captainMenuBtn = document.getElementById('captain-menu-btn');
    const captainMenu = document.getElementById('captain-menu');
    const captainMenuContainer = document.querySelector('.captain-menu-container');
    // Обработчик для кнопки капитанов
    captainMenuBtn.addEventListener('click', function() {
        captainMenuContainer.classList.toggle('active');
    });
    // Закрытие меню при клике вне его области
    document.addEventListener('click', function(event) {
        if (!captainMenuContainer.contains(event.target)) {
            captainMenuContainer.classList.remove('active');
        }
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const adminMenuBtn = document.getElementById('admin-menu-btn');
    const adminMenu = document.getElementById('admin-menu');
    const adminMenuContainer = document.querySelector('.admin-menu-container');
    // Обработчик для кнопки капитанов
    adminMenuBtn.addEventListener('click', function() {
        adminMenuContainer.classList.toggle('active');
    });
    // Закрытие меню при клике вне его области
    document.addEventListener('click', function(event) {
        if (!adminMenuContainer.contains(event.target)) {
            adminMenuContainer.classList.remove('active');
        }
    });
});
// Открытие панели при клике на кнопку
document.getElementById("login-button").addEventListener("click", function() {
    const modal = document.getElementById("login-modal");
    modal.style.display = "block";
    document.querySelector(".auth-form").style.display = "block";
    document.querySelector(".register-form").style.display = "none";
    document.getElementById("email").value = '';
    document.getElementById("password").value = '';
    document.getElementById("register-email").value = '';
    document.getElementById("register-password").value = '';
    document.getElementById("confirm-password").value = '';
});
// Закрытие панели при клике на кнопку закрытия
document.getElementById("close-button").addEventListener("click", function() {
    document.getElementById("login-modal").style.display = "none";
    // Сброс формы при закрытии
    document.querySelector(".auth-form form").reset();
    document.querySelector(".register-form form").reset();
});
// Переключение между формами входа и регистрации
document.getElementById("register-link").addEventListener("click", function() {
    document.querySelector(".auth-form").style.display = "none";
    document.querySelector(".register-form").style.display = "block";
});
// Обработка отправки формы (пока без логики обработки)
document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();
    alert("Вход выполнен!");
});
document.querySelector(".register-form form").addEventListener("submit", function(event) {
    event.preventDefault();
    alert("Регистрация выполнена!");
});
document.addEventListener('DOMContentLoaded', function () {
    const loginButton = document.getElementById('login-button');
    const profileMenu = document.getElementById('profile-menu');
    const profileIcon = document.getElementById('profile-icon');
    const loginModal = document.getElementById('login-modal');
    const closeButton = document.getElementById('close-button');
    const loginForm = document.getElementById('login-form');
    // Открытие модального окна для входа
    loginButton.addEventListener('click', () => {
        loginModal.style.display = 'block';
    });
    // Закрытие модального окна
    closeButton.addEventListener('click', () => {
        loginModal.style.display = 'none';
    });
    // Замена кнопки "Войти" на иконку профиля
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        // Проверка простого ввода (можно заменить на серверную логику)
        if (email && password) {
            // Закрываем модальное окно
            loginModal.style.display = 'none';

            // Прячем кнопку "Войти" и показываем иконку профиля
            loginButton.style.display = 'none';
            profileMenu.style.display = 'inline-block';
        }
    });
    // Открытие выпадающего меню профиля
    profileIcon.addEventListener('click', () => {
        const dropdown = document.querySelector('.profile-dropdown');
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    });
    // Закрытие меню профиля при клике вне его
    document.addEventListener('click', function (event) {
        const dropdown = document.querySelector('.profile-dropdown');
        if (!profileMenu.contains(event.target)) {
            dropdown.style.display = 'none';
        }
    });
});
document.addEventListener('DOMContentLoaded', function () {
    const calculateRouteButton = document.getElementById('calculate-route');
    const buyTicketButton = document.getElementById('buy-ticket');

    // Флаг для проверки, рассчитан ли маршрут
    let isRouteCalculated = false;

    // Обработчик для кнопки "Рассчитать маршрут"
    calculateRouteButton.addEventListener('click', () => {
        const fromStation = document.getElementById('from-station').value;
        const toStation = document.getElementById('to-station').value;

        if (!fromStation || !toStation || fromStation === toStation) {
            alert("Выберите корректные станции отправления и назначения!");
            return;
        }

        // Логика расчёта маршрута (пример)
        isRouteCalculated = true; // Фиксируем, что маршрут рассчитан
        buyTicketButton.disabled = false; // Активируем кнопку "Купить билет"

        alert("Маршрут успешно рассчитан!");
    });

    // Обработчик для кнопки "Купить билет"
    buyTicketButton.addEventListener('click', () => {
        if (isRouteCalculated) {
            alert("Покупка билета завершена!");
        } else {
            alert("Пожалуйста, рассчитайте маршрут перед покупкой билета.");
        }
    });
});
    // Сброс данных (при необходимости очистить токены или куки)
    alert("Вы вышли из системы!");
