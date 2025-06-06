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
        if (!response.ok) {
            throw new Error(`登录失败: ${response.status}`);
        }
        return await response.json();
    },

    // 获取用户信息
    getUserInfo: async (username: string): Promise<any> => {
        const response = await fetch(`${API_BASE_URL}/info/${username}`);
        if (!response.ok) {
            throw new Error(`获取用户信息失败: ${response.status}`);
        }
        const res = await response.json();
        if (res.status === 200) {
            return res.data;
        } else {
            throw new Error(res.message || '获取用户信息失败');
        }
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
        if (!response.ok) {
            throw new Error(`更新用户信息失败: ${response.status}`);
        }
        return await response.json();
    },

    // 上传头像
    uploadAvatar: async (persion_id: string, file: File): Promise<any> => {
        const formData = new FormData();
        formData.append('persion_id', persion_id);
        formData.append('file', file);
        console.log('uploadAvatar上传头像:', persion_id, file);
        const response = await fetch(`${API_BASE_URL}/info/upload_avatar`, {
            method: 'POST',
            body: formData,
        });
        const result = await response.json();
        if (result.status === 200 && result.avatar) {
            return result;
        } else {
            throw new Error(result.detail || '头像上传失败');
        }
    },

    // 获取文件列表
    getTablesList: async (): Promise<any> => {
        const response = await fetch(`${API_BASE_URL}/table/list_preview`);
        if (!response.ok) {
            throw new Error(`获取文件列表失败: ${response.status}`);
        }
        return await response.json();
    },

    // 获取文件下载URL
    getFilePreviewUrl: (filename: string): string => {
        return `${API_BASE_URL}/table/preview/${filename}`;
    },

    // 自动填表
    autoFillTable: async (filename: string, personIds: string[] = []): Promise<any> => {
        console.log('开始自动填表1:', filename);
        console.log('开始自动填表2:', personIds);
        const response = await fetch(`${API_BASE_URL}/table/autofill`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ table_name: filename, persons: personIds }),
        });
        if (!response.ok) {
            throw new Error(`自动填表失败: ${response.status}`);
        }
        return await response.json();
    },

    // 可以添加更多API请求方法
};
