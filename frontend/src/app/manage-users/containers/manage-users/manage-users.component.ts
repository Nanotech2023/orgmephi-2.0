import { Component, OnInit, ViewChild } from '@angular/core'
import { UserFull } from '@api/users/models'
import { ManageUsersStore } from '@/manage-users/manage-users.store'
import { Observable } from 'rxjs'
import { DxDataGridComponent } from 'devextreme-angular'
import { UsersService } from '@api/users/users.service'


@Component( {
    selector: 'app-manage-users',
    templateUrl: './manage-users.component.html',
    styleUrls: [ './manage-users.component.scss' ],
    providers: [ ManageUsersStore ]
} )
export class ManageUsersComponent implements OnInit
{
    @ViewChild( DxDataGridComponent, { static: false } ) grid!: DxDataGridComponent
    users$: Observable<UserFull[]> = this.store.users$
    selectedRowIndex = -1

    constructor( private store: ManageUsersStore, private usersService: UsersService ) {}

    ngOnInit(): void
    {
        this.store.reload()
    }

    editRow(): void
    {
        this.grid.instance.editRow( this.selectedRowIndex )
        this.grid.instance.deselectAll()
    }

    deleteRow(): void
    {
        this.grid.instance.deleteRow( this.selectedRowIndex )
        this.grid.instance.deselectAll()
    }

    addRow(): void
    {
        this.grid.instance.addRow()
        this.grid.instance.deselectAll()
    }

    selectedChanged( e: any ): void
    {
        this.selectedRowIndex = e.component.getRowIndexByKey( e.selectedRowKeys[ 0 ] )
    }
}
