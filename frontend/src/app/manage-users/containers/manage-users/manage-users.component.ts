import { Component, OnInit, ViewChild } from '@angular/core'
import { SchoolRegistrationRequestUser, User } from '@api/users/models'
import { fixedHeight } from '@/shared/consts'
import { AgGridAngular } from 'ag-grid-angular'
import { ManageUsersStore } from '@/manage-users/manage-users.store'
import { Observable } from 'rxjs'


@Component( {
    selector: 'app-manage-users',
    templateUrl: './manage-users.component.html',
    styleUrls: [ './manage-users.component.scss' ],
    providers: [ ManageUsersStore ]
} )
export class ManageUsersComponent implements OnInit
{
    minContainerHeight: number = fixedHeight
    columnDefs = [
        { field: 'id', sortable: true, filter: true, headerName: 'ID' },
        { field: 'username', sortable: true, filter: true, headerName: 'Имя пользовтаеля' },
        { field: 'role', sortable: true, filter: true, headerName: 'Роль' },
        { field: 'type', sortable: true, filter: true, headerName: 'Тип регистрации' }
    ]
    addUserVisible: boolean = false
    editUserVisible: boolean = false
    editingUser: any = null
    users$: Observable<User[]> = this.store.users$
    @ViewChild( 'table_users' ) agGrid!: AgGridAngular

    constructor( private store: ManageUsersStore ) {}

    ngOnInit(): void
    {
        this.store.reload()
    }

    onUserAdd( requestRegistration: SchoolRegistrationRequestUser ): void
    {
        this.store.add( requestRegistration )
    }

    showEditUserModal(): void
    {
        const selectedRows = this.agGrid.api.getSelectedRows()
        if ( selectedRows.length !== 0 )
        {
            this.editingUser = selectedRows[ 0 ]
            this.editUserVisible = true
        }
    }

    resetEditingUser( $event: boolean ): void
    {
        if ( $event == false )
        {
            this.editingUser = null
            this.agGrid.api.deselectAll()
        }
    }

    onUserEdit( user: User ): void
    {
        this.store.edit( user )
    }

    getRowNodeId( data: User ): number | undefined
    {
        return data.id
    }
}
