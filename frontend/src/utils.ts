export function buildHierarchy(disciplines) 
{
        const map = new Map();
        const result = [];

        disciplines.forEach(d => map.set(d.id, { ...d, label: d.name, value: d.id }));

        disciplines.forEach(d => {
                if (d.parent_id !== null && map.has(d.parent_id)) {
                const parent = map.get(d.parent_id);
                map.get(d.id).label = `${parent.label} > ${d.name}`;
                } else {
                result.push(map.get(d.id)); // Only top-level disciplines
                }
        });

        return Array.from(map.values());
};