const { createApp, ref, onMounted, computed, watch } = Vue
const { debounce } = _;
const app = createApp({
    setup() {
        const loading = ref(true)
        const latitude = ref(0)
        const longitude = ref(0)
        const locationError = ref("")
        const selectCityHelperOption = {
            name: 'Select a city',
            latitude: 0,
            longitude: 0,
            timezone: ''
        }
        const selectedCity = ref(selectCityHelperOption)
        const cities = [
            selectCityHelperOption,
            {
                name: "George Town, Cayman Islands",
                latitude: 19.2869,
                longitude: -81.3671,
                timezone: "America/Cayman"
            },
            {
                name: "London, United Kingdom",
                latitude: 51.5074,
                longitude: 0.1278,
                timezone: "Europe/London"
            },
            {
                name: "New York, United States",
                latitude: 40.7128,
                longitude: -74.0060,
                timezone: "America/New_York"
            },
            {
                name: "Tokyo, Japan",
                latitude: 35.6762,
                longitude: 139.6503,
                timezone: "Asia/Tokyo"
            },
            {
                name: "Paris, France",
                latitude: 48.8566,
                longitude: 2.3522,
                timezone: "Europe/Paris"
            },
            {
                name: "Singapore, Singapore",
                latitude: 1.3521,
                longitude: 103.8198,
                timezone: "Asia/Singapore"
            },
            {
                name: "Dubai, United Arab Emirates",
                latitude: 25.2048,
                longitude: 55.2708,
                timezone: "Asia/Dubai"
            },
            {
                name: "Kuala Lumpur, Malaysia",
                latitude: 3.1390,
                longitude: 101.6869,
                timezone: "Asia/Kuala_Lumpur"
            },
            {
                name: "Istanbul, Turkey",
                latitude: 41.0082,
                longitude: 28.9784,
                timezone: "Europe/Istanbul"
            },
            {
                name: "Seoul, South Korea",
                latitude: 37.5665,
                longitude: 126.9780,
                timezone: "Asia/Seoul"
            },
            {
                name: "Hong Kong, Hong Kong",
                latitude: 22.3193,
                longitude: 114.1694,
                timezone: "Asia/Hong_Kong"
            },
            {
                name: "Moscow, Russia",
                latitude: 55.7558,
                longitude: 37.6173,
                timezone: "Europe/Moscow"
            },
            {
                name: "Bangkok, Thailand",
                latitude: 13.7563,
                longitude: 100.5018,
                timezone: "Asia/Bangkok"
            },
            {
                name: "Amsterdam, Netherlands",
                latitude: 52.3667,
                longitude: 4.8945,
                timezone: "Europe/Amsterdam"
            },
            {
                name: "Delhi, India",
                latitude: 28.7041,
                longitude: 77.1025,
                timezone: "Asia/Kolkata"
            },
            {
                name: "Toronto, Canada",
                latitude: 43.6532,
                longitude: -79.3832,
                timezone: "America/Toronto"
            },
            {
                name: "Rome, Italy",
                latitude: 41.9028,
                longitude: 12.4964,
                timezone: "Europe/Rome"
            },
            {
                name: "Sydney, Australia",
                latitude: -33.8688,
                longitude: 151.2093,
                timezone: "Australia/Sydney"
            },
            {
                name: "Los Angeles, United States",
                latitude: 34.0522,
                longitude: -118.2437,
                timezone: "America/Los_Angeles"
            },
            {
                name: "Chicago, United States",
                latitude: 41.8781,
                longitude: -87.6298,
                timezone: "America/Chicago"
            },

        ]
        const getLocation = () => {
            loading.value = true;
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function (position) {

                    latitude.value = position.coords.latitude;
                    longitude.value = position.coords.longitude;
                    loading.value = false;
                }, function (error) {
                    loading.value = false;
                    switch (error.code) {
                        case error.PERMISSION_DENIED:
                            locationError.value = "Request for Geolocation was denied"
                            break;
                        case error.POSITION_UNAVAILABLE:
                            locationError.value = "Location information is unavailable."
                            break;
                        case error.TIMEOUT:
                            locationError.value = "The request to get user location timed out."
                            break;
                        case error.UNKNOWN_ERROR:
                            locationError.value = "An unknown error occurred."
                            break;
                    }
                });
            }
            else {
                alert("Geolocation is not supported by this browser.");
                loading.value = false;
            }
        }
        const timezone = ref('EST')
        const availableTimezones = ['EST', 'CST', 'MST', 'PST']
        const fajrIshaMethod = ref("1")
        const availableFajrIshaMethods = []
        const asrMethod = ref("jomhor")
        const availableAsrMethods = ['jomhor', 'hanafi']
        const commonParams = computed(() => {
            const params = new URLSearchParams();
            params.append('latitude', latitude.value);
            params.append('longitude', longitude.value);
            params.append('timezone', timezone.value);
            params.append('fajr_isha_method', fajrIshaMethod.value);
            params.append('asr_fiqh', asrMethod.value);
            params.append('threshold', 1);
            return params;
        })
        const urls = computed(() => {
            const param = commonParams.value;
            const base = window.location.href + "is_adhan_time?" + param.toString();
            return {
                fajr: base + "&name=fajr",
                dohr: base + "&name=dohr",
                asr: base + "&name=asr",
                maghreb: base + "&name=maghreb",
                ishaa: base + "&name=ishaa",
                all: base,
            }
        })
        const prayerTimes = ref({
            fajr: '',
            dohr: '',
            asr: '',
            maghreb: '',
            ishaa: '',
        })
        const prayerTimeLoading = ref(false)
        const fetchPrayerTimes = debounce(() => {
            prayerTimeLoading.value = true;
            const params = commonParams.value;
            fetch('/show_adhan_times' + "?" + params.toString())
                .then(response => response.json())
                .then(data => {
                    prayerTimes.value = data;
                }).finally(() => {
                    prayerTimeLoading.value = false;
                });
        }, 100)
        const fetchAllTimezones = () => {
            // get it from openapi spec at /openapi.json
            fetch('/openapi.json')
                .then(response => response.json())
                .then(data => {
                    availableTimezones.splice(0, availableTimezones.length, ...data.components.schemas.Timezone.enum)
                });
        }
        const fetchAllFajrIshaMethods = () => {
            // get it from openapi spec at /openapi.json
            fetch('/openapi.json')
                .then(response => response.json())
                .then(data => {
                    
                    // data.components.schemas.Methods.enum
                    // data.components.schemas.Methods.description  split by \n each line starts with "- <n>: <description>"
                    // n is enum value
                    const newAvailableFajrIshaMethods = data.components.schemas.Methods.enum.map((value, index) => {

                        const alldescription = data.components.schemas.Methods.description.split("\n").filter((line)=> line.split(':', 1)[0].indexOf(value) != -1).map((line) => line.split(':', 2)[1])
                        console.log('for', value, alldescription)
                        const description = data.components.schemas.Methods.description.split("\n")
                        .filter((line)=> line.split(':', 1)[0].indexOf(value) != -1)
                        .map((line) => line.split(":", 2)[1])[0]

                        return {
                            value,
                            description
                        }
                    })

                    availableFajrIshaMethods.splice(0, availableFajrIshaMethods.length, ...newAvailableFajrIshaMethods)
                });
        }
        const copyToClipboard = (url) => {
            navigator.clipboard.writeText(url)
        }
        const reportHref = computed(() => {
            return `mailto:zkhan1093@gmail.com?subject=Adhan Time API - Report Incorrect Adan Time&body=Adhan Time for my location identified by lon (${longitude.value}) and lat (${latitude.value}) with parameters URL: ${urls.value.all}. The Adhan time is incorrect. Please fix it. It should be the following on Date: ${new Date().toISOString()} \n\nFajr: 00:00\n Dohr: 00:00\n Asr: 00:00\n Maghreb: 00:00\n Isha: 00:00\n\n  <Please set correct values above>\n\n\nJazakAllah Khair`
        })
        watch(timezone, fetchPrayerTimes)
        watch(latitude, fetchPrayerTimes)
        watch(longitude, fetchPrayerTimes)
        watch(fajrIshaMethod, fetchPrayerTimes)
        watch(asrMethod, fetchPrayerTimes)
        watch(selectedCity, () => {
            if (selectedCity.value.name !== selectCityHelperOption.name) {
                latitude.value = selectedCity.value.latitude
                longitude.value = selectedCity.value.longitude
                timezone.value = selectedCity.value.timezone
            }
        })
        // initializations
        fetchAllTimezones()
        fetchAllFajrIshaMethods()
        fetchPrayerTimes()
        getLocation()

        return {
            loading,
            timezone,
            prayerTimes,
            urls,
            availableTimezones,
            prayerTimeLoading,
            latitude,
            longitude,
            cities,
            selectedCity,
            reportHref,
            getLocation,
            copyToClipboard,
            locationError,
            fajrIshaMethod,
            availableFajrIshaMethods,
            asrMethod,
            availableAsrMethods,
        }
    }
})
app.mount('#app')
