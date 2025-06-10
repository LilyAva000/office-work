// API请求工具
// 注意！！路径中/的拼接，多余的/会导致请求失败
const BASE_URL = 'http://127.0.0.1:8008';
const API_BASE_URL = BASE_URL + '/api';

export const apiClient = {
    BASE_URL,
    API_BASE_URL,

    // 登录方法
    login: async (username: string, password: string): Promise<any> => {
        const response = await fetch(`${API_BASE_URL}/user/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                password
            }),
        });
        return await response.json();
    },

    // 获取用户信息
    getUserInfo: async (username: string): Promise<any> => {
        const response = await fetch(`${API_BASE_URL}/info/${username}`);
        return await response.json();
    },

    // 更新用户信息
    updateUserInfo: async (username: string, userInfo: any): Promise<any> => {
        const response = await fetch(`${API_BASE_URL}/info/${username}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                person_info: userInfo
            }),
        });
        return await response.json();
    },

    // 上传头像
    uploadAvatar: async (personId: string, file: File): Promise<any> => {
        const formData = new FormData();
        formData.append('person_id', personId);
        formData.append('file', file);
        const response = await fetch(`${API_BASE_URL}/info/upload_avatar`, {
            method: 'POST',
            body: formData,
        });
        return await response.json();
    },

    // 获取文件列表
    getTablesList: async (): Promise<any> => {
        const response = await fetch(`${API_BASE_URL}/table/list_preview`);
        return await response.json();
    },

    // 获取文件下载URL
    getFilePreviewUrl: (filename: string): string => {
        return `${API_BASE_URL}/table/preview/${filename}`;
    },

    // 自动填表
    autoFillTable: async (filename: string, personIds: string[] = []): Promise<any> => {
        const response = await fetch(`${API_BASE_URL}/table/autofill`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ table_name: filename, persons: personIds }),
        });
        return await response.json();
    },

    // 可以添加更多API请求方法
};
