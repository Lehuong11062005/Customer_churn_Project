import { useEffect, useState } from 'react';
import { getMe } from '../../services/authApi';

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const response = await getMe();
        setProfile(response.data);
      } catch (error) {
        console.error('Failed to load profile:', error);
      } finally {
        setLoading(false);
      }
    };
    loadProfile();
  }, []);

  if (loading) {
    return <div className="p-6 text-center">Loading profile...</div>;
  }

  if (!profile) {
    return <div className="p-6 text-center">Profile not found</div>;
  }

  const getRoleBadgeColor = (role) => {
    const colors = {
      admin: 'bg-red-100 text-red-800',
      manager: 'bg-blue-100 text-blue-800',
      staff: 'bg-green-100 text-green-800',
    };
    return colors[role] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-6">My Profile</h1>
      <div className="max-w-2xl rounded-xl bg-white p-6 shadow">
        <div className="grid gap-6">
          <div>
            <label className="text-sm text-gray-600">Username</label>
            <p className="text-lg font-semibold">{profile.username}</p>
          </div>
          <div>
            <label className="text-sm text-gray-600">Full Name</label>
            <p className="text-lg font-semibold">{profile.full_name || '-'}</p>
          </div>
          <div>
            <label className="text-sm text-gray-600">Email</label>
            <p className="text-lg font-semibold">{profile.email || '-'}</p>
          </div>
          <div>
            <label className="text-sm text-gray-600">Role</label>
            <p className="text-lg">
              <span className={`inline-block rounded-full px-3 py-1 text-sm font-semibold ${getRoleBadgeColor(profile.role)}`}>
                {profile.role}
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
