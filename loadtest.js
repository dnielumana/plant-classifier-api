import http from 'k6/http';
import { check, sleep } from 'k6';

const imageData = open('./test_image.jpg', 'b');

export const options = {
    vus: 20,
    duration: '15s',
};

export default function () {
    const data = {
        file: http.file(imageData, 'test_image.jpg'),
    };

const res = http.post('http://13.217.7.17:8000/classify', data);

    check(res, {
        'status is 200': (r) => r.status === 200,
    });

    sleep(0.5);
}