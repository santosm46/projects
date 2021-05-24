
const DEFAULT_PATH = 'database';

const dbExample = {
    1: {
        name: 'Maria',
        birth_date: 827366400000,
        mother_id: null,
        father_id: null,
    },
    2: {
        name: 'José',
        birth_date: 827366400000,
        mother_id: null,
        father_id: null,
    },
    3: {
        name: 'Fulano',
        birth_date: 827366400000,
        mother_id: 1,
        father_id: 2,
    },

};

function getMemberAge(member) {
    const date = new Date();
    const birth_date = new Date(member.birth_date);
    return date.getFullYear()-birth_date.getFullYear();
}

class LocalFile  {
    constructor() {
        this.familyTree = dbExample;
    }

    getMember(memberId) {
        return this.familyTree[memberId];
    }

}

class DbFile {
    constructor(fileName) {
        const familyTree
    }
}



